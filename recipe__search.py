# -*- coding: utf-8 -*-

import sys
import json
import twitter
from recipe__oauth_login import oauth_login

def search(t, q=None, max_batches=5, count=100):

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = t.search.tweets(q=q, count=count)

    statuses = search_results['statuses']

    # Iterate through more batches of results by following the cursor
    for _ in range(max_batches):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
            # Create a dictionary from next_results, which has the following form:
            # ?max_id=313519052523986943&q=%23MentionSomeoneImportantForYou&include_entities=1
            kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
            search_results = twitter_api.search.tweets(**kwargs)
            statuses += search_results['statuses']

    return statuses


if __name__ == '__main__':
    Q = ' '.join(sys.argv[1:])

    t = oauth_login()
    statuses = search(t, q=Q)
    print json.dumps(statuses, indent=1)
