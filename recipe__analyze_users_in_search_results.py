# -*- coding: utf-8 -*-

import sys
import twitter
from recipe__get_user_info import get_info_by_screen_name
from recipe__oauth_login import oauth_login

def analyze_users_in_search_results(t, q, max_pages=15, results_per_page=100):

    # Search for something

    search_api = twitter.Twitter(domain="search.twitter.com")
    search_results = []
    for page in range(1,max_pages+1):
        search_results += \
            search_api.search(q=q, rpp=results_per_page, page=page)['results']

    # Extract the screen names (the "from_user" field) from the results
    # and optionally map them to a useful field like the tweet id
    # See http://code.google.com/p/twitter-api/issues/detail?id=214 for 
    # why you can't use the user id values.

    screen_name_to_tweet_ids = {}
    for result in search_results:

        screen_name = result['from_user']

        if not screen_name_to_tweet_ids.has_key(screen_name):
            screen_name_to_tweet_ids[screen_name] = []

        screen_name_to_tweet_ids[screen_name] += [ result['id'] ]


    # Use the /users/lookup resource to resolve profile information for 
    # these screen names

    screen_name_to_info = get_info_by_screen_name(t, screen_name_to_tweet_ids.keys())

    # Extract the home location for each user. Note that the "location" field can 
    # be anything a user has typed in, and may be something like "Everywhere", 
    # "United States" or something else that won't geocode to a specific coordinate 
    # on a map.

    screen_name_to_location = dict([(sn, info['location']) 
                                    for sn, info in screen_name_to_info.items()])

    # Use the various screen_name_to{tweet_ids, info, location} maps to determine 
    # interesting things about the people who appear in the search results.

    return screen_name_to_info, screen_name_to_location, screen_name_to_tweet_ids

if __name__ == '__main__':

    Q = ' '.join(sys.argv[1:])

    # Don't forget to pass in keyword parameters if you don't have
    # a token file stored to disk

    t = oauth_login()

    sn2info, sn2location, sn2tweet_ids = analyze_users_in_search_results(t, Q)

    # Go off and do interesting things...
