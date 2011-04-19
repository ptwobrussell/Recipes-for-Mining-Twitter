# -*- coding: utf-8 -*-

# A simple pattern created to illustrate geocoding for Where 2.0 (2011)
# Get your Google Maps API Key from http://code.google.com/apis/maps/signup.html

import geopy
GOOGLE_MAPS_API_KEY = ''
g = geopy.geocoders.Google(GOOGLE_MAPS_API_KEY)


transforms = [('Greater ', ''), 
                           (' Area', ''), 
                           ('San Francisco Bay', 'San Francisco')] # etc.

locations = ['Greater Nashville Area',
                       'San Francisco Bay'] # from LinkedIn data

cache = {}
for location in locations:
    if cache.has_key(location): # Preserve API calls
        continue

    for transform in transforms:
        results = g.geocode(location, exactly_one=False)
        cache[location] = [r for r in results][0][1]
        break

import json
print json.dumps(cache, indent=2)
