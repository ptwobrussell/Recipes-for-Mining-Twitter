# -*- coding: utf-8 -*-

import os
import sys
import twitter
import networkx as nx
from recipe__create_rt_graph import create_rt_graph
from recipe__oauth_login import oauth_login
from recipe__search import search

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

    # Your output

    OUT = 'twitter_retweet_graph.dot'

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

    # Write Graphviz output

    if not os.path.isdir('out'):
        os.mkdir('out')

    f = os.path.join(os.getcwd(), 'out', OUT)

    write_dot_output(g, f)

    print >> sys.stderr, \
            'Try this on the DOT output: $ dot -Tpng -O%s %s' % (f, f,)
