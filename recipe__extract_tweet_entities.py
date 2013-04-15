# -*- coding: utf-8 -*-

import json
from recipe__oauth_login import oauth_login
from recipe__search import search

def get_entities(tweet):
    return tweet['entities']

if __name__ == '__main__':
    t = oauth_login()
    tweets = search(t, "Python", max_batches=1, count=10) # Use "Python" as a sample query to get some tweets to process
    entities = [ get_entities(tweet) for tweet in tweets ]

    print json.dumps(entities, indent=1)
