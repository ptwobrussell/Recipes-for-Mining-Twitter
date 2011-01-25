# -*- coding: utf-8 -*-

import json
import twitter

t = twitter.Twitter(domain='api.twitter.com', api_version='1')

print json.dumps(t.trends(), indent=1)
