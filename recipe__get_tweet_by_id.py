# -*- coding: utf-8 -*-

import sys
import json
import twitter

TWEET_ID = sys.argv[1] # Example: 24877908333961216

t = twitter.Twitter(domain='api.twitter.com', api_version='1')

# No authentication required, but rate limiting is enforced

tweet = t.statuses.show(id=TWEET_ID, include_entities=1) 

print json.dumps(tweet, indent=1)
