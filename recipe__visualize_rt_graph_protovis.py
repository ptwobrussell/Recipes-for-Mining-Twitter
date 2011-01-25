# -*- coding: utf-8 -*-

import sys
import os
import json
import webbrowser
import twitter
from recipe__create_rt_graph import create_rt_graph

# Your query
Q = sys.argv[1]

# How many pages of data to grab for the search results
NUM_PAGES = 5

# How many search results per page
RESULTS_PER_PAGE = 100

# An HTML page that we'll inject Protovis consumable data into
HTML_TEMPLATE = 'etc/twitter_retweet_graph.html'
OUT = os.path.basename(HTML_TEMPLATE)

# Writes out an HTML page that can be opened in the browser
# that displays a graph 
def write_protovis_output(g, out_file):
    nodes = g.nodes()
    indexed_nodes = {}

    idx = 0
    for n in nodes:
        indexed_nodes.update([(n, idx,)])
        idx += 1

    links = []
    for n1, n2 in g.edges():
        links.append({'source' : indexed_nodes[n2], 
                      'target' : indexed_nodes[n1]})

    json_data = json.dumps({"nodes" : [{"nodeName" : n} for n in nodes], "links" : links}, indent=4)
    html = open(HTML_TEMPLATE).read() % (json_data,)
    if not os.path.isdir('out'):
        os.mkdir('out')
    f = open(os.path.join(os.getcwd(), 'out', out_file), 'w')
    f.write(html)
    f.close()

    print >> sys.stderr, 'Data file written to: %s' % f.name

    return f.name

if __name__ == '__main__':

    # Your query

    Q = sys.argv[1]

    # How many pages of data to grab for the search results

    NUM_PAGES = 5

    # How many search results per page

    RESULTS_PER_PAGE = 100

    # Get some search results for a query

    twitter_search = twitter.Twitter(domain='search.twitter.com')
    search_results = []
    for page in range(1,NUM_PAGES):
        search_results.append(twitter_search.search(q=Q, rpp=RESULTS_PER_PAGE, page=page))

    all_tweets = [tweet for page in search_results for tweet in page['results']]

    # Build up a graph data structure

    g = create_rt_graph(all_tweets)

    # Write Protovis output and open in browser

    protovis_output = write_protovis_output(g, OUT)
    webbrowser.open('file://' + protovis_output)
