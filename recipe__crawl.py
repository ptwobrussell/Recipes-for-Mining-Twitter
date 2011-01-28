# -*- coding: utf-8 -*-

import sys
import redis
from recipe__make_twitter_request import make_twitter_request
from recipe__setwise_operations import get_redis_id
from recipe__oauth_login import oauth_login


def crawl_followers(t, r, follower_ids, limit=1000000, depth=2):

    # Helper function

    def get_all_followers_ids(user_id, limit):

        cursor = -1
        ids = []
        while cursor != 0:

            response = make_twitter_request(t, t.followers.ids,
                                            user_id=user_id, cursor=cursor)

            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']

            print >> sys.stderr, 'Fetched %i total ids for %s' % (len(ids), user_id)

            # Consider storing the ids to disk during each iteration to provide an 
            # an additional layer of protection from exceptional circumstances

            if len(ids) >= limit or response is None:
                break

        return ids

    for fid in follower_ids:

        next_queue = get_all_followers_ids(fid, limit)

        # Store a fid => next_queue mapping in Redis or other database of choice
        # In Redis, it might look something like this:

        rid = get_redis_id('follower_ids', user_id=fid)
        [ r.sadd(rid, _id) for _id in next_queue ]

        d = 1
        while d < depth:
            d += 1
            (queue, next_queue) = (next_queue, [])
            for _fid in queue:
                _follower_ids = get_all_followers_ids(user_id=_fid, limit=limit)

                # Store a fid => _follower_ids mapping in Redis or other 
                # database of choice. In Redis, it might look something like this:

                rid = get_redis_id('follower_ids', user_id=fid)
                [ r.sadd(rid, _id) for _id in _follower_ids ] 

                next_queue += _follower_ids

if __name__ == '__main__':

    SCREEN_NAME = sys.argv[1]

    # Remember to pass in keyword parameters if you don't have a
    # token file stored on disk already

    t = oauth_login()

    # Resolve the id for SCREEN_NAME

    _id = str(t.users.show(screen_name=SCREEN_NAME)['id'])

    crawl_followers(t, redis.Redis(), [_id])

    # The total number of nodes visited represents one measure of potential influence.
    # You can also use the user => follower ids information to create a 
    # graph for analysis
