# -*- coding: utf-8 -*-

import json
import twitter
from recipe__extract_tweet_entities import getEntities

MAX_PAGES = 15
RESULTS_PER_PAGE = 100

t = twitter.Twitter(domain='api.twitter.com', api_version='1')

trends = [ 
            trend['name'] 
                for trend in t.trends()['trends'] 
         ]

idx = 0
for trend in trends:
    print '[%i] %s' % (idx, trend,)
    idx += 1

trend_idx = int(raw_input('\nPick a trend: '))

q = trends[trend_idx]

print 'Fetching tweets for %s...' % (q, )

twitter_search = twitter.Twitter(domain="search.twitter.com")
search_results = []
for page in range(1,MAX_PAGES+1):
    search_results += [ twitter_search.search(q=q, rpp=RESULTS_PER_PAGE, page=page) ]

for page in search_results:
    for tweet in page['results']:
        tweet['entities'] = getEntities(tweet)

f = open('search_results.json', 'w')
f.write(json.dumps(search_results, indent=1))
f.close()
