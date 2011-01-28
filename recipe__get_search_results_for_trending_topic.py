# -*- coding: utf-8 -*-

import os
import sys
import json
import twitter
from recipe__extract_tweet_entities import get_entities

MAX_PAGES = 15
RESULTS_PER_PAGE = 100

# Get the trending topics

t = twitter.Twitter(domain='api.twitter.com', api_version='1')

trends = [ 
            trend['name'] 
                for trend in t.trends()['trends'] 
         ]

idx = 0
for trend in trends:
    print '[%i] %s' % (idx, trend,)
    idx += 1

# Prompt the user

trend_idx = int(raw_input('\nPick a trend: '))

q = trends[trend_idx]

# Search

print >> sys.stderr, 'Fetching tweets for %s...' % (q, )

twitter_search = twitter.Twitter(domain="search.twitter.com")

search_results = []
for page in range(1,MAX_PAGES+1):
    search_results += \
        twitter_search.search(q=q, rpp=RESULTS_PER_PAGE, page=page)['results']

# Exract tweet entities and embed them into search results

for result in search_results:
        result['entities'] = get_entities(result)

if not os.path.isdir('out'):
        os.mkdir('out')

f = open(os.path.join(os.getcwd(), 'out', 'search_results.json'), 'w')
f.write(json.dumps(search_results, indent=1))
f.close()

print >> sys.stderr, "Entities for tweets about trend '%s' saved to %s" % (q, f.name,)
