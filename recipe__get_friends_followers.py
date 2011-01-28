# -*- coding: utf-8 -*-

import sys
import twitter
from recipe__make_twitter_request import make_twitter_request
import functools

SCREEN_NAME = sys.argv[1]
MAX_IDS = int(sys.argv[2])

if __name__ == '__main__':

    # Not authenticating lowers your rate limit to 150 requests per hr. 
    # Authenticate to get 350 requests per hour.

    t = twitter.Twitter(domain='api.twitter.com', api_version='1')

    # You could call make_twitter_request(t, t.friends.ids, *args, **kw) or 
    # use functools to "partially bind" a new callable with these parameters

    get_friends_ids = functools.partial(make_twitter_request, t, t.friends.ids)

    # Ditto if you want to do the same thing to get followers...

    # getFollowerIds = functools.partial(make_twitter_request, t, t.followers.ids)

    cursor = -1
    ids = []
    while cursor != 0:

        # Use make_twitter_request via the partially bound callable...

        response = get_friends_ids(screen_name=SCREEN_NAME, cursor=cursor)
        ids += response['ids']
        cursor = response['next_cursor']

        print >> sys.stderr, 'Fetched %i total ids for %s' % (len(ids), SCREEN_NAME)

        # Consider storing the ids to disk during each iteration to provide an 
        # an additional layer of protection from exceptional circumstances

        if len(ids) >= MAX_IDS:
            break

    # Do something useful with the ids like store them to disk...

    print ids 
