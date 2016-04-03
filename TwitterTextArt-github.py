# Python Art - Twitter Text Art
#
# This code generates Python Turtle text from a Twitter feed
#
# The project has been inspired and helped through lots of examples and questions on forums or websites including:
#   http://stackoverflow.com/questions/743806/split-string-into-a-list-in-python
#   http://stackoverflow.com/questions/17371652/tweepy-twitter-api-not-returning-all-search-results?rq=1
#   http://stackoverflow.com/questions/15141031/python-turtle-draw-text-with-on-screen-with-larger-font
#   http://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
#
# Thanks to these programmers!
#
# CC0 Ian Simpson, 2nd April 2016 @familysimpson

import tweepy
import turtle
import random

Ckey = '...' # Put your own credentials here
Csec = '...'
Akey = '...'
Asec = '...'

lstTweet = []

def processTweets(tweet):
    global lstTweet
    # split string into individual words
    tmpWords = tweet.split()
    # append to lstTweet
    for word in tmpWords:
        lstTweet.append(word)

def sortTweets():
    global lstTweet
    lstTweet.sort()

def purgeTweets():
    # remove any tweets that start with a non alphabetic character e.g. hashtags, mentions, etc.
    global lstTweet
    tmpTweet = []
    for words in lstTweet:
        if (ord(words[0])<65) or (ord(words[0])>122) or (words[0:4]=="http"):
            print(ord(words[0]))
        else:
            tmpTweet.append(words)
    lstTweet = tmpTweet


auth = tweepy.OAuthHandler(Ckey, Csec)
auth.set_access_token(Akey, Asec)
twapi = tweepy.API(auth)

for status in tweepy.Cursor(twapi.home_timeline).items(10):
    # Process a single status
    processTweets(status.text)
sortTweets()
purgeTweets()

# Another alternative is:
#for tweet in tweepy.Cursor(twapi.search,
#                           q="#python",
#                           count=100,
#                           result_type="recent",
#                           include_entities=True,
#                           lang="en").items(10):
#    processTweets(tweet.text)

wn = turtle.Screen()
w = wn.window_width()
h = wn.window_height()

t1 = turtle.Turtle()

for word in lstTweet:
    t1.color(192/255.,192/255.,192/255.) # silver lines
    t1.goto(random.randrange(int(-(w/2)),int(w/2)), random.randrange(int(-(h/2)),int(h/2)))
    t1.color(random.randrange(0,255)/255.,random.randrange(0,255)/255.,random.randrange(0,255)/255.)
    fontsize = random.randrange(8,32)
    t1.write(word, False, font=("Palatino", fontsize, "normal"))



wn.exitonclick()
