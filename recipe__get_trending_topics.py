# -*- coding: utf-8 -*-

import json
import twitter
from recipe__oauth_login import oauth_login

t = oauth_login()
WORLD_WOE_ID = 1 # The Yahoo! Where On Earth ID for the entire world
world_trends = t.trends.place(_id=WORLD_WOE_ID) # get back a callable

# call the callable and iterate through the trends returned
print json.dumps(world_trends, indent=1)
