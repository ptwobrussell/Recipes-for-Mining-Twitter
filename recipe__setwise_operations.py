# -*- coding: utf-8 -*-

import sys
import functools
import twitter
import locale
import redis
from recipe__make_twitter_request import make_twitter_request

# A convenience function for consistently creating keys for a 
# screen name, user id, or anything else you'd like

def get_redis_id(key_name, screen_name=None, user_id=None):

    if screen_name is not None:
        return 'screen_name$' + screen_name + '$' + key_name
    elif user_id is not None:
        return 'user_id$' + user_id + '$' + key_name
    else:
        raise Exception("No screen_name or user_id provided to get_redis_id")

if __name__ == '__main__':

    SCREEN_NAME = sys.argv[1]
    MAX_IDS = int(sys.argv[2])

    # Create a client to connect to a running redis-server with default
    # connection settings. It is recommended that you run Redis in 
    # "append only mode" -- Search for "appendonly yes" in redis.conf for details.

    r = redis.Redis()

    # Not authenticating lowers your rate limit to 150 requests per hr. 
    # Authenticate to get 350 requests per hour.

    t = twitter.Twitter(domain='api.twitter.com', api_version='1')

    # Harvest some friend ids

    get_friends_ids = functools.partial(make_twitter_request, t, t.friends.ids)

    cursor = -1
    ids = []
    while cursor != 0:

        # Use make_twitter_request via the partially bound callable...

        response = get_friends_ids(screen_name=SCREEN_NAME, cursor=cursor)

        # Add the ids to the set in redis with the sadd (set add) operator

        rid = get_redis_id('friend_ids', screen_name=SCREEN_NAME)

        [ r.sadd(rid, _id) for _id in response['ids'] ]

        cursor = response['next_cursor']

        print >> sys.stderr, \
            'Fetched %i total friend ids for %s' % (r.scard(rid), SCREEN_NAME)

        if r.scard(rid) >= MAX_IDS:
            break

    # Harvest some follower ids

    get_followers_ids = functools.partial(make_twitter_request, t, t.followers.ids)

    cursor = -1
    ids = []
    while cursor != 0:

        # Use make_twitter_request via the partially bound callable...

        response = get_followers_ids(screen_name=SCREEN_NAME, cursor=cursor)

        # Add the ids to the set in redis with the sadd (set add) operator

        rid = get_redis_id('follower_ids', screen_name=SCREEN_NAME)

        [ r.sadd(rid, _id) for _id in response['ids'] ]

        cursor = response['next_cursor']

        print >> sys.stderr, \
            'Fetched %i total follower ids for %s' % (r.scard(rid), SCREEN_NAME)

        if r.scard(rid) >= MAX_IDS:
            break

    # Compute setwise operations the data in Redis

    n_friends = r.scard(get_redis_id('friend_ids', screen_name=SCREEN_NAME))

    n_followers = r.scard(get_redis_id('follower_ids', screen_name=SCREEN_NAME))

    n_friends_diff_followers = r.sdiffstore('temp',
                                            [get_redis_id('friend_ids', 
                                            screen_name=SCREEN_NAME),
                                            get_redis_id('follower_ids', 
                                            screen_name=SCREEN_NAME)])
    r.delete('temp')

    n_followers_diff_friends = r.sdiffstore('temp',
                                            [get_redis_id('follower_ids', 
                                            screen_name=SCREEN_NAME),
                                            get_redis_id('friend_ids',
                                            screen_name=SCREEN_NAME)])
    r.delete('temp')

    n_friends_inter_followers = r.sinterstore('temp',
            [get_redis_id('follower_ids', screen_name=SCREEN_NAME),
            get_redis_id('friend_ids', screen_name=SCREEN_NAME)])
    r.delete('temp')

    print '%s is following %s' % (SCREEN_NAME, locale.format('%d', n_friends, True))

    print '%s is being followed by %s' % (SCREEN_NAME, locale.format('%d',
                                          n_followers, True))

    print '%s of %s are not following %s back' % (locale.format('%d',
            n_friends_diff_followers, True), locale.format('%d', n_friends, True),
            SCREEN_NAME)

    print '%s of %s are not being followed back by %s' % (locale.format('%d',
            n_followers_diff_friends, True), locale.format('%d', n_followers, True),
            SCREEN_NAME)

    print '%s has %s mutual friends' \
        % (SCREEN_NAME, locale.format('%d', n_friends_inter_followers, True))
