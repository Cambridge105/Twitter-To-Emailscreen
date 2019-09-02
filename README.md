# Twitter-To-Emailscreen
Publish tweets to the studio email screen

## Installation instructions
First off, you need to install the python-twitter library  
`pip install python-twitter`

Then, clone this repo to pick up the main python routine

Then, you'll need the two config files t.py and e.py. These contain secrets for Twitter and Email integration respectively. 
Should you need to recreate them, the format of t.py is:

    ACCESS_TOKEN_KEY = "xxx"
    ACCESS_TOKEN_SECRET = "xxx"
    CONSUMER_KEY = "xxx"
    CONSUMER_SECRET = "xxx"
    
Note, you can regenerate these keys from developer.twitter.com but you must be logged in as @cambridge105 to do it - otherwise your personal mentions will end up on the studio screens as they are locked to the authenticated user!

The format of e.py is:

    EMAIL_HOST = "mail.cambridge105.fm" 
    EMAIL_PORT = "465"
    EMAIL_USER = "xxx"
    EMAIL_PASSWORD = "xxx"
    
You can get credentials for this from Steve.

The final file you need is lastTweetId.py 
This stores the IDs of the last tweets, which ensures we don't duplicate tweets between runs. The format of the file is:

    LAST_ID_SKY = 123456789123456789
    LAST_ID_105 = 123456789123456789
    LAST_ID_105_MENTIONS = 123456789123456789
    LAST_ID_IRN = 123456789123456789
   
You can look at tweet URLs on the twitter website to work out where you want to start from if you need to recreate this.

Finally, set it to run in a cronjob. Beware - our not-for-profit plan allows us 15 API calls per 15 minutes it appears. Each run of the file is 4 API calls, so we shouldn't run it more than every 5 minutes. 
`*/5 * * * * /usr/bin/python /path/to/getTweets.py`
The script prints emailed tweets to stdout for debugging, so you may wish to redirect that to /dev/null 
