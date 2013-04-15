# -*- coding: utf-8 -*-

import sys
import twitter
from recipe__get_user_info import get_info_by_screen_name
from recipe__oauth_login import oauth_login
from recipe__search import search

def analyze_users_in_search_results(t, q, max_batches=5, count=100):

    # Search for something

    statuses = search(t, q=q, max_batches=max_batches, count=count)

    # Extract the screen names from the results
    # and optionally map them to a useful field like the tweet id

    screen_name_to_tweet_ids = {}
    screen_name_to_info = {}
    screen_name_to_location = {}
    for status in statuses:

        screen_name = status['user']['screen_name']

        if not screen_name_to_tweet_ids.has_key(screen_name):
            screen_name_to_tweet_ids[screen_name] = []
        screen_name_to_tweet_ids[screen_name] += [ status['id'] ]

        screen_name_to_info[screen_name] = status['user']

        screen_name_to_location[screen_name] = status['user']['location']

    # Note that the "location" field can 
    # be anything a user has typed in, and may be something like "Everywhere", 
    # "United States" or something else that won't geocode to a specific coordinate 
    # on a map.

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
    print sn2info
    print 
    print sn2location
    print
    print sn2tweet_ids
