# -*- coding: utf-8 -*-

import re

def get_rt_origins(tweet):

    # Regex adapted from 
    # http://stackoverflow.com/questions/655903/python-regular-expression-for-retweets

    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    rt_origins = []

    # Inspect the tweet to see if was produced with /statuses/retweet/:id
    # See http://dev.twitter.com/doc/post/statuses/retweet/:id
    
    if tweet.has_key('retweet_count'):
        if tweet['retweet_count'] > 0:
            rt_origins += [ tweet['user']['name'].lower() ]

    # Also, inspect the tweet for the presence of "legacy" retweet patterns such as "RT" and "via"

    try:
        rt_origins += [ mention.strip() for mention in rt_patterns.findall(tweet['text'])[0][1].split() ]
    except IndexError, e:
        pass

    # Filter out any duplicates

    return list(set([rto.strip("@").lower() for rto in rt_origins]))
