# -*- coding: utf-8 -*-

import json
import twitter

t = twitter.Twitter(domain='api.twitter.com', api_version='1')

WORLD_WOE_ID = 1 # The Yahoo! Where On Earth ID for the entire world

world_trends = t.trends._(WORLD_WOE_ID) # get back a callable

# call the callable and iterate through the trends returned
print json.dumps([ trend for trend in world_trends()[0]['trends'] ], indent=1) 
