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
    
    # A mocked up array of tweets for purposes of illustration.
    # Assume tweets have been fetched from the /search resource or elsewhere.

    tweets = \
    [
       {
        'text' : 'RT @ptowbrussell Get @SocialWebMining at http://bit.ly/biais2 #w00t'

        # ... more tweet fields ...

       },

       {
        'text' : 'Get @SocialWebMining example code at http://bit.ly/biais2 #w00t',
        'retweet_count' : 1,
        'user' : { 
         'name' : 'ptwobrussell'

            # ... more user fields ...
        }

        # ... more tweet fields ...

       },

       # ... more tweets ...

    ]

    for tweet in tweets:
        print get_rt_origins(tweet) 
