# Twitter bot


# Import libraies
import codecs
import sys
import time
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from ncr import *

follow_users = ['', '', '', '']

# Twitter credentials
# Consumer key
ckey = ''
# Consumer secret
csecret = ''
# Access token
atoken = ''
# Access secret
asecret = ''

#specialChars = {'Å':b'\x5D', 'å':b'\x7D', 'Æ':b'\x5B', 'æ':b'\x7B', 'Ø':b'\x5C', 'ø':b'\x7C'} # Adafruit thermal printer Set Danish
specialChars = {'Å':b'\x8f', 'å':b'\x86', 'Æ':b'\x92', 'æ':b'\x91', 'Ø':b'\x9d', 'ø':b'\x9b'} #NCR Character table 1
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


# Connect to the printer
p = ThermalPrinter()
# NCR Uses 1, Adafruit thermal uses 4
p.setcharset(1)


# Define print method for adafruit printer
#def print_tweet(timestamp, user, tweet):
#    p.inverseOn()
#    p.println(user)
#    p.inverseOff()
#    p.underlineOn()
#    p.println(timestamp)
#    p.underlineOff()
#    p.println(tweet)
#    p.feed(3)
#    p.fullcut()

# Define print method for NCR printer
def print_tweet(timestamp, user, tweet):
    p.inverse_on()
    p.print_text(user)
    p.inverse_off()
    p.print_text('\n')
    p.underline_on()
    p.print_text(timestamp)
    p.underline_off()
    p.print_text('\n')
    p.print_text(tweet)
    p.print_text('\n')
    p.linefeed(10)
    #p.fullcut()



class listener(StreamListener):

    def on_data(self, data):
        try:
            # Load the data as json object
            theJSON = json.loads(data)

            # Extract what we want from the object
            timestamp  = str(theJSON['created_at'])
            user = str(('@') + theJSON['user']['screen_name'])
            tweet = str(theJSON['text'].encode('utf-8',errors='ignore'))
            if (tweet.startswith("RT")) != True:
                tweet = replace_all(tweet, specialChars)
                print (timestamp)
                print (user)
                print (tweet)

                # Print the tweet
                print_tweet(timestamp, user, tweet)

            return True

        except BaseException, e:
            print 'failed ondata:',str(e)
            time.sleep(5)

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(follow = follow_users)