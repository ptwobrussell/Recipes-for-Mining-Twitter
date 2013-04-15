# Extract geo coordinates from search results

import sys
import twitter
from recipe__oauth_login import oauth_login
from recipe__search import search

Q = ' '.join(sys.argv[1:])

t = oauth_login()
statuses = search(t, q=Q, max_batches=10, count=100)

# Extract geocoordinates from tweets in search results

coords =  [ status['geo'] for status in statuses if status['geo'] is not None ]

print coords
