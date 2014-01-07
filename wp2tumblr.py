"""
wp2tumblr.py
============
By Francis Tseng,
For Python 2.7

Import Wordpress posts (in an XML export) into Tumblr.
Based on Jon Thorton's wp2tumblr.py.

README
======

1. Install the only dependency:
    $ pip install oauth2

2. Register an application on your Tumblr account to
   get your consumer key and consumer secret:
    http://www.tumblr.com/oauth/apps

3. Get your access token and access secret for your account here:
    https://api.tumblr.com/console//calls/user/info

4. In your Wordpress blog, go to Tools > Export, select 'Posts' and download
   the export file.

5. Set the proper values in this script:
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BLOG, and WP_XML

6. Run the script:
    $ python wp2tumblr.py
"""



from urllib import urlencode
import urlparse
import time
from datetime import datetime
from xml.dom import minidom
import oauth2 as oauth

TUMBLR = 'https://api.tumblr.com/v2/blog/'
CONSUMER_KEY = 'your-consumer-key'
CONSUMER_SECRET = 'your-consumer-secret'
ACCESS_TOKEN = 'your-access-token'
ACCESS_SECRET = 'your-access-secret'
BLOG = 'somename.tumblr.com'
WP_XML = 'wpexport.xml'
request_token_url = 'http://www.tumblr.com/oauth/request_token'
access_token_url = 'http://www.tumblr.com/oauth/access_token'
authorize_url = 'http://www.tumblr.com/oauth/authorize'

consumer = oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
token = oauth.Token(ACCESS_TOKEN, ACCESS_SECRET)
client = oauth.Client(consumer, token)

# Create a new post on Tumblr.
def post(body, title=None, type='text', state='published', tags='', date=None):
    endpoint = TUMBLR + BLOG + '/post'
    if date is None:
        date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S GMT')
    params = {
            'type': type,
            'state': state,
            'tags': tags,
            'date': date,
            'title': title,
            'body': body,
            'oauth_version': '1.0',
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_token': ACCESS_TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
    }

    req = oauth.Request(method='POST', url=endpoint, parameters=params)
    sig_method = oauth.SignatureMethod_HMAC_SHA1()
    req.sign_request(sig_method, consumer, token)
    print(params)
    data = urlencode(params).encode('utf-8')
    resp, content = client.request(endpoint, 'POST', data)
    if resp['status'] != '201':
        raise Exception('Post creation failed.')

# For convenience.
def get_value(item, tag_name):
    el = item.getElementsByTagName(tag_name)[0]
    if len(el.childNodes) == 0:
        return ''
    else:
        return el.firstChild.nodeValue

# Start parsing.
dom = minidom.parse(WP_XML)
items = dom.getElementsByTagName('item')

print('Total posts: %s' % items.length)

# If something goes wrong, you can uncomment this line
# and set N to the index of the post that failed.
# This will start creating new posts from that post on.
#items = items[N:]

for idx, i in enumerate(items):

    # Only published posts.
    if get_value(i, 'wp:status') != 'publish':
        continue

    title = get_value(i, 'title').strip().encode('utf-8', 'xmlcharrefreplace')
    date = get_value(i, 'pubDate')
    body = get_value(i, 'content:encoded').encode('utf-8', 'xmlcharrefreplace')
    tags = ', '.join([el.firstChild.nodeValue.encode('utf-8') for el in i.getElementsByTagName('category')])

    print(idx)
    post(body, title=title, date=date, tags=tags)

