#!/usr/bin/python

import sys
sys.path.append('/home/pi/105tweets/')

import twitter
from t import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET
api = twitter.Api(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,access_token_key=ACCESS_TOKEN_KEY,access_token_secret=ACCESS_TOKEN_SECRET,tweet_mode='extended')

import re

import smtplib
from e import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
emailserv = smtplib.SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT)
emailserv.login(EMAIL_USER, EMAIL_PASSWORD)

from lastTweetId import LAST_ID_SKY, LAST_ID_105, LAST_ID_IRN, LAST_ID_105_MENTIONS

def formatEmail(msgSubj, msgText):
    msg = "From: Twitter <twitter@cambridge105.co.uk>\r\nTo: <studio@cambridge105.co.uk>\r\nSubject: " + msgSubj + "\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Disposition: inline\r\nContent-Transfer-Encoding: 8bit\r\n\r\n" + msgText
    msg = re.sub(ur'https?:\/\/\S* ', u'', msg)
    return msg.encode('latin-1',errors='ignore')

last_id_sky = LAST_ID_SKY
last_id_105 = LAST_ID_105
last_id_105_mentions = LAST_ID_105_MENTIONS
last_id_irn = LAST_ID_IRN
ids_changed = 0

blacklisted_tweeters = ['Lord_Drainlid']

# Get tweets from Sky News Break
statuses = api.GetUserTimeline(87416722,since_id=LAST_ID_SKY,exclude_replies=False)
for s in statuses:
   #print s.full_text + ' (ID:' + str(s.id) + ')'
   msg = formatEmail('Breaking news from @SkyNewsBreak', s.full_text)
   emailserv.sendmail('twitter@cambridge105.co.uk','studio@cambridge105.co.uk',msg)
   if (last_id_sky == LAST_ID_SKY):
     last_id_sky = s.id
     ids_changed = 1

# Get tweets & replies from Cambridge 105
statuses = api.GetUserTimeline(95086990,since_id=LAST_ID_105,exclude_replies=False)
for s in statuses:
   #print s.full_text + ' (ID:' + str(s.id) + ')'
   msg = formatEmail('Tweet from @' + s.user.screen_name, s.full_text)
   emailserv.sendmail('twitter@cambridge105.co.uk','studio@cambridge105.co.uk',msg)
   if (last_id_105 == LAST_ID_105):
     last_id_105 = s.id
     ids_changed = 1

# Get mentions for Cambridge 105
mentions = api.GetMentions(since_id=LAST_ID_105_MENTIONS)
for m in mentions:
   if m.user.screen_name not in blacklisted_tweeters:
     #print m.full_text + ' (ID:' + str(m.id) + ')'
     msg = formatEmail('Tweet from ' + m.user.name + ' - @' + m.user.screen_name, m.full_text)
     emailserv.sendmail('twitter@cambridge105.co.uk','studio@cambridge105.co.uk',msg)
     if (last_id_105_mentions == LAST_ID_105_MENTIONS):
       last_id_105_mentions = m.id
       ids_changed = 1

# Get tweets from IRN
statuses = api.GetUserTimeline(312059464,since_id=LAST_ID_IRN,exclude_replies=True)
for s in statuses:
   #print s.full_text + ' (ID:' + str(s.id) + ')'
   msg = formatEmail('News trail from Sky News Radio', s.full_text)
   emailserv.sendmail('twitter@cambridge105.co.uk','studio@cambridge105.co.uk',msg)
   if (last_id_irn == LAST_ID_IRN):
     last_id_irn = s.id
     ids_changed = 1	 


	 
# Set the last updated IDs so the next run doesn't duplicate them
if (ids_changed == 1):
  f = open("/home/pi/105tweets/lastTweetId.py", "w")
  f.write("LAST_ID_SKY = " + str(last_id_sky) + "\r\nLAST_ID_105 = " + str(last_id_105) + "\r\nLAST_ID_105_MENTIONS = " + str(last_id_105_mentions) + "\r\nLAST_ID_IRN = " + str(last_id_irn))
  f.close()
