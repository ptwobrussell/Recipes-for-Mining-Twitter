# -*- coding: utf-8 -*-

import os
import sys
import networkx as nx
import redis
import twitter

from recipe__setwise_operations import get_redis_id

SCREEN_NAME = sys.argv[1]

t = twitter.Twitter(api_version='1', domain='api.twitter.com')

_id = str(t.users.show(screen_name=SCREEN_NAME)['id'])

g = nx.Graph()      # An undirected graph
r = redis.Redis()

# Compute all ids for nodes appearing in the graph. Let's assume you've
# adapted recipe__crawl to harvest all of the friends and friends' friends
# for a user so that you can build a graph to inspect how these 
# friendships relate to one another

# Create a collection of ids for a person and all of this person's friends

ids = [_id] + list(r.smembers(get_redis_id('friend_ids', user_id=_id)))

# Process each id in the collection such that edges are added to the graph
# for each of current_id's friends if those friends are also
# friends of SCREEN_NAME. In the end, you get a "hub and spoke" graph of
# SCREEN_NAME and SCREEN_NAME's friends, but you also see connections that
# existing amongst SCREEN_NAME's friends as well

for current_id in ids:

    print >> sys.stderr, 'Processing user with id', current_id

    try:
        friend_ids = list(r.smembers(get_redis_id('friend_ids', user_id=current_id)))
        friend_ids = [fid for fid in friend_ids if fid in ids]
    except Exception, e:
        print >> sys.stderr, 'Encountered exception. Skipping', current_id

    for friend_id in friend_ids:
        print >> sys.stderr, 'Adding edge %s => %s' % (current_id, friend_id,)
        g.add_edge(current_id, friend_id)

# Optionally, pickle the graph to disk...

if not os.path.isdir('out'):
    os.mkdir('out')

f = os.path.join('out', SCREEN_NAME + '-friendships.gpickle')
nx.write_gpickle(g, f)

print >> sys.stderr, 'Pickle file stored in', f
