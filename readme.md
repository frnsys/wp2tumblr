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