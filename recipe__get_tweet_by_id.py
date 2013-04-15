# -*- coding: utf-8 -*-

import sys
import json
import twitter
from recipe__oauth_login import oauth_login

TWEET_ID = sys.argv[1] # Example: 24877908333961216

t = oauth_login()

# No authentication required, but rate limiting is enforced

tweet = t.statuses.show(id=TWEET_ID, include_entities=1) 

print json.dumps(tweet, indent=1)
