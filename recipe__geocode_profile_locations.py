# -*- coding: utf-8 -*-

import sys
from urllib2 import HTTPError
import geopy
from recipe__oauth_login import oauth_login
from recipe__analyze_users_in_search_results import analyze_users_in_search_results

def geocode_locations(geocoder, locations):

    # Some basic replacement transforms may be necessary for geocoding services to function properly
    # You may probably need to add your own as you encounter rough edges in the data or with the geocoding
    # service you settle on. For example, ...

    replacement_transforms = [('San Francisco Bay', 'San Francisco')]

    location_to_coords = {}
    location_to_description = {}

    for location in locations:

        # Avoid unnecessary I/O with a simple cache

        if location_to_coords.has_key(location):
            continue

        transformed_location = location

        for transform in replacement_transforms:

            transformed_location = transformed_location.replace(*transform)

            while True:

                num_errors = 0

                try:
                    # This call returns a generator

                    results = geocoder.geocode(transformed_location, exactly_one=False)
                    break
                except HTTPError, e:
                    num_errors += 1
                    if num_errors >= MAX_HTTP_ERRORS:
                        sys.exit()
                    print >> sys.stderr, e.message
                    print >> sys.stderr, 'Encountered an urllib2 error. Trying again...'
                except UnicodeEncodeError, e:
                    print >> sys.stderr, e
                    print >> sys.stderr, 'Encountered a UnicodeEncodeError...', e.message
                    break
                except geopy.geocoders.google.GQueryError, e:
                    print >> sys.stderr, e
                    print >> sys.stderr, 'Encountered a ...GQueryError', e.message
                    break
                  

        for result in results:

            # Each result is of the form ("Description", (X,Y))
            # Unless you have a some special logic for picking the best of many possible
            # results, choose the first one returned in results and move along

            location_to_coords[location] = result[1]
            location_to_description[location] = result[0]
            break

    # Use location_to_coords and other information of interest to populate a visualization.
    # Depending on your particular needs, it is highly likely that you'll want to further
    # post process the geocoded locations to filter out locations such as "U.S.A." which will
    # plot a placemarker in the geographic center of the United States yet make the visualization
    # look skewed in favor of Oklahoma, for example.

    return location_to_coords, location_to_description

if __name__ == '__main__':

    # Use your own API key here if you use a geocoding service
    # such as Google or Yahoo!

    GEOCODING_API_KEY = sys.argv[1]

    Q = ' '.join(sys.argv[2:])

    MAX_HTTP_ERRORS = 100

    g = geopy.geocoders.Google(GEOCODING_API_KEY)

    # Don't forget to pass in keyword parameters if you don't have
    # a token file stored to disk

    t = oauth_login()

    # This function returns a few useful maps. Let's use the screen_name => location map and
    # geocode the locations

    _, screen_name_to_location, _ = analyze_users_in_search_results(t, Q, 2)

    locations = screen_name_to_location.values()
    location2coords, location2description = geocode_locations(g, locations)
