# -*- coding: utf-8 -*-

#XXX: TEST ME

import sys
import functools
import redis
from recipe__make_twitter_request import make_twitter_request
from recipe__setwise_operations import getRedisId
from recipe__oauth_login import oauth_login

ID = sys.argv[1]

t = oauth_login()

r = redis.Redis()

def getAllFollowerIds(user_id, limit):

    cursor = -1
    ids = []
    while cursor != 0:

        response = make_twitter_request(t, t.followers.ids, user_id=user_id, cursor=cursor)
        ids += response['ids']
        cursor = response['next_cursor']

        print >> sys.stderr, 'Fetched %i total ids for %s' % (len(ids), user_id)

        # Consider storing the ids to disk during each iteration to provide an 
        # an additional layer of protection from exceptional circumstances

        if len(ids) >= limit:
            return ids

def crawlFollowers(follower_ids, limit=1000000, depth=2):

    for fid in follower_ids:

        next_queue = getAllFollowerIds(fid, limit)

        # Store a fid => next_queue mapping in Redis or other database of choice
        # In Redis, it might look something like this:

        rid = getRedisId('follower_ids', user_id=fid)
        [ r.sadd(rid, _id) for _id in next_queue ]

        d = 1
        while d < depth:
            d += 1
            (queue, next_queue) = (next_queue, [])
            for _fid in queue:
                _follower_ids = getAllFollowerIds(user_id=_fid, limit=limit)

                # Store a fid => _follower_ids mapping in Redis or other database of choice
                # In Redis, it might look something like this:

                rid = getRedisId('follower_ids', user_id=fid)
                [ r.sadd(rid, _id) for _id in _follower_ids ] 

                next_queue += _follower_ids

crawlFollowers([ID])

# The total number of nodes visited represents one measure of potential influence.
# You can also use the information user => follower id information to create a 
# graph that can be analyzed.
