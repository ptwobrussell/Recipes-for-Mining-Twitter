# -*- coding: utf-8 -*-

import sys
import json
import twitter
import networkx as nx
from recipe__get_rt_origins import get_rt_origins
from recipe__search import search
from recipe__oauth_login import oauth_login

def create_rt_graph(tweets):

    g = nx.DiGraph()

    for tweet in tweets:

        rt_origins = get_rt_origins(tweet)

        if not rt_origins:
            continue

        for rt_origin in rt_origins:
            g.add_edge(rt_origin.encode('ascii', 'ignore'), 
                       tweet['user']['screen_name'].encode('ascii', 'ignore'), 
                       {'tweet_id': tweet['id']}
            )

    return g

if __name__ == '__main__':

    # Your query

    Q = ' '.join(sys.argv[1])

    # How many batches of data to grab for the search results

    MAX_BATCHES = 2

    # How many search results per page

    COUNT = 100

    # Get some search results for a query
    t = oauth_login()
    search_results = search(t, q=Q, max_batches=MAX_BATCHES, count=COUNT)
    g = create_rt_graph(search_results)

    # Print out some stats

    print >> sys.stderr, "Number nodes:", g.number_of_nodes()
    print >> sys.stderr, "Num edges:", g.number_of_edges()
    print >> sys.stderr, "Num connected components:", \
                         len(nx.connected_components(g.to_undirected()))
    print >> sys.stderr, "Node degrees:", sorted(nx.degree(g))
