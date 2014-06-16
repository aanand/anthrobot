import os
import tweepy
from bot import util

auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)

q = " OR ".join("'%s'" % t for t in util.SEARCH_SEEDS)

i = None
for searches in range(5):
    print i
    tweets = api.search(q, max_id=i, count=100)
    i = tweets[-1].id

    for a in util.create_actions(t.text for t in tweets):
        print a
