# -*- coding: utf-8 -*-

import sys
import json
import twitter
import networkx as nx
from recipe__get_rt_origins import get_rt_origins

def create_rt_graph(tweets):

    g = nx.DiGraph()

    for tweet in tweets:

        rt_origins = get_rt_origins(tweet)

        if not rt_origins:
            continue

        for rt_origin in rt_origins:
            g.add_edge(rt_origin.encode('ascii', 'ignore'), 
                       tweet['from_user'].encode('ascii', 'ignore'), 
                       {'tweet_id': tweet['id']}
            )

    return g

if __name__ == '__main__':

    # Your query

    Q = ' '.join(sys.argv[1])

    # How many pages of data to grab for the search results

    MAX_PAGES = 15

    # How many search results per page

    RESULTS_PER_PAGE = 100

    # Get some search results for a query

    twitter_search = twitter.Twitter(domain='search.twitter.com')
    search_results = []
    for page in range(1,MAX_PAGES+1):
        search_results.append(
            twitter_search.search(q=Q, rpp=RESULTS_PER_PAGE, page=page)
        )

    all_tweets = [tweet for page in search_results for tweet in page['results']]

    # Build up a graph data structure

    g = create_rt_graph(all_tweets)

    # Print out some stats

    print >> sys.stderr, "Number nodes:", g.number_of_nodes()
    print >> sys.stderr, "Num edges:", g.number_of_edges()
    print >> sys.stderr, "Num connected components:", 
                         len(nx.connected_components(g.to_undirected()))
    print >> sys.stderr, "Node degrees:", sorted(nx.degree(g))
