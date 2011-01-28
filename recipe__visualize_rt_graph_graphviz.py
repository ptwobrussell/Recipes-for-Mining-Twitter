# -*- coding: utf-8 -*-

import os
import sys
import twitter
import networkx as nx
from recipe__create_rt_graph import create_rt_graph

# Writes out a DOT language file that can be converted into an 
# image by Graphviz

def write_dot_output(g, out_file):

    try:
        nx.drawing.write_dot(g, out_file)
        print >> sys.stderr, 'Data file written to', out_file
    except ImportError, e:

        # Help for Windows users:
        # Not a general purpose method, but representative of
        # the same output write_dot would provide for this graph
        # if installed and easy to implement

        dot = ['"%s" -> "%s" [tweet_id=%s]' % (n1, n2, g[n1][n2]['tweet_id'])
               for (n1, n2) in g.edges()]
        f = open(out_file, 'w')
        f.write('''strict digraph {
    %s
    }''' % (';\n'.join(dot), ))
        f.close()

        print >> sys.stderr, 'Data file written to: %s' % f.name

if __name__ == '__main__':

    # Your query

    Q = ' '.join(sys.argv[1])

    # Your output

    OUT = 'twitter_retweet_graph'

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

    # Write Graphviz output

    if not os.path.isdir('out'):
        os.mkdir('out')

    f = os.path.join(os.getcwd(), 'out', OUT)

    write_dot_output(g, f)

    print >> sys.stderr, \
            'Try this on the DOT output: $ dot -Tpng -O%s %s.dot' % (f, f,)
