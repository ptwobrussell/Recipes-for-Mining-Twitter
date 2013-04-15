# -*- coding: utf-8 -*-

import re
from recipe__oauth_login import oauth_login
from recipe__search import search

def get_rt_origins(tweet):

    # Regex adapted from 
    # http://stackoverflow.com/questions/655903/python-regular-expression-for-retweets

    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    rt_origins = []

    # Inspect the tweet to see if was produced with /statuses/retweet/:id
    # See http://dev.twitter.com/doc/post/statuses/retweet/:id
    
    if tweet.has_key('retweeted_status'):
        rt_origins += [ tweet['retweeted_status']['user']['screen_name'].lower() ]

    # Also, inspect the tweet for the presence of "legacy" retweet 
    # patterns such as "RT" and "via"

    try:
        rt_origins += [ 
                        mention.strip() 
                        for mention in rt_patterns.findall(tweet['text'])[0][1].split() 
                      ]
    except IndexError, e:
        pass

    # Filter out any duplicates

    return list(set([rto.strip("@").lower() for rto in rt_origins]))

if __name__ == '__main__':

    t = oauth_login()
    tweets = search(t, q='Python', max_batches=1, count=100)


    for tweet in tweets:
        print tweet['text'], get_rt_origins(tweet) 
