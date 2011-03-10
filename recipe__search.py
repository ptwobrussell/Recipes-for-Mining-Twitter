# -*- coding: utf-8 -*-

import sys
import json
import twitter

Q = ' '.join(sys.argv[1:])

MAX_PAGES = 15
RESULTS_PER_PAGE = 100

twitter_search = twitter.Twitter(domain="search.twitter.com")

search_results = []
for page in range(1,MAX_PAGES+1):
    search_results += \
        twitter_search.search(q=Q, rpp=RESULTS_PER_PAGE, page=page)['results']

print json.dumps(search_results, indent=1)
