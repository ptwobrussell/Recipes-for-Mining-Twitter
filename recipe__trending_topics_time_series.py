# -*- coding: utf-8 -*-

import os
import datetime
import time
import json
import twitter

t = twitter.Twitter(domain='api.twitter.com', api_version='1')

if not os.path.isdir('trends_data'):
        os.mkdir('trends_data')

while True:
    now = str(datetime.datetime.now())

    trends = json.dumps(t.trends(), indent=1)

    f = open(os.path.join(os.getcwd(), 'trends_data', now), 'w')
    f.write(trends)
    f.close()

    time.sleep(60) # 60 seconds
