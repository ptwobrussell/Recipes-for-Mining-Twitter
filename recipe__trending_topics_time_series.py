# -*- coding: utf-8 -*-

import os
import sys
import datetime
import time
import json
import twitter

t = twitter.Twitter(domain='api.twitter.com', api_version='1')

if not os.path.isdir('out/trends_data'):
        os.makedirs('out/trends_data')

while True:

    now = str(datetime.datetime.now())

    trends = json.dumps(t.trends(), indent=1)

    f = open(os.path.join(os.getcwd(), 'out', 'trends_data', now), 'w')
    f.write(trends)
    f.close()

    print >> sys.stderr, "Wrote data file", f.name
    print >> sys.stderr, "Zzz..."

    time.sleep(60) # 60 seconds
