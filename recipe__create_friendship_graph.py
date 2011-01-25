# -*- coding: utf-8 -*-

# XXX: TEST ME

import os
import sys
import networkx as nx
import redis

from recipe__setwise_operations import getRedisId

ID = sys.argv[1]

g = nx.Graph() # An undirected graph
r = redis.Redis()

# Compute all ids for nodes appearing in the graph. Let's assume you've
# used recipe__crawl to harvest *all of the frienships* that exist
# for a group of users so that you can build a graph to see how these 
# friendships relate to one another in a graph

# Create a collection of ids for a seed user and all of this user's friends

ids = [ID] + list(r.smembers(getRedisId('friend_ids', user_id=ID)))

# Process each id in the collection such that edges are added to the graph
# for each of current_id's friends, but only if those friends are also
# friends of ID

for current_id in ids:
    print >> sys.stderr, 'Processing user with id', current_id

    try:
        friend_ids = list(r.smembers(getRedisId('friend_ids', user_id=current_id)))
        friend_ids = [fid for fid in friend_ids if fid in ids]
    except Exception, e:
        print >> sys.stderr, 'Encountered exception. Skipping', current_id

    for friend_id in friend_ids:
        g.add_edge(current_id, friend_id)

# Optionally, pickle the graph to disk...

if not os.path.isdir('out'):
    os.mkdir('out')

filename = os.path.join('out', ID + 'friendships.gpickle')
nx.write_gpickle(g, filename)

print 'Pickle file stored in: %s' % filename
