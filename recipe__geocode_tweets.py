# Extract geo coordinates from search results

import sys
import twitter
from recipe__oauth_login import oauth_login

Q = ' '.join(sys.argv[1:])

def get_search_results(t, q, max_pages=15, results_per_page=100):

    # Search for something

    search_api = twitter.Twitter(domain="search.twitter.com")
    search_results = []
    for page in range(1,max_pages+1):
        search_results += \
            search_api.search(q=q, rpp=results_per_page, page=page)['results']

    return search_results

t = oauth_login()

search_results = get_search_results(t, Q, max_pages=2)

# Extract geocoordinates from tweets in search results

coords =  [ t['geo'] for t in search_results if t['geo'] is not None ]

print coords
