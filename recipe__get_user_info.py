# -*- coding: utf-8 -*-

from recipe__oauth_login import oauth_login
from recipe__make_twitter_request import make_twitter_request

# Assume ids have been fetched from a scenario such as the
# one presented in recipe__get_friends_followers.py and that
# t is an authenticated instance of twitter.Twitter

def get_info_by_id(t, ids):

    id_to_info = {}

    while len(ids) > 0:

        # Process 100 ids at a time...

        ids_str = ','.join([str(_id) for _id in ids[:100]])
        ids = ids[100:]

        response = make_twitter_request(t, 
                                      getattr(getattr(t, "users"), "lookup"),
                                      user_id=ids_str)
     
        if response is None:
            break

        if type(response) is dict:  # Handle Twitter API quirk
            response = [response]

        for user_info in response:
            id_to_info[user_info['id']] = user_info

        return id_to_info

# Similarly, you could resolve the same information by screen name 
# using code that's virtually identical. These two functions
# could easily be combined.

def get_info_by_screen_name(t, screen_names):

    sn_to_info = {}

    while len(screen_names) > 0:

        # Process 100 ids at a time...

        screen_names_str = ','.join([str(sn) for sn in screen_names[:100]])
        screen_names = screen_names[100:]

        response = make_twitter_request(t, 
                                      getattr(getattr(t, "users"), "lookup"),
                                      screen_name=screen_names_str)
     
        if response is None:
            break

        if type(response) is dict:  # Handle Twitter API quirk
            response = [response]

        for user_info in response:
            sn_to_info[user_info['screen_name']] = user_info

        return sn_to_info

if __name__ == '__main__':

    # Be sure to pass in any necessary keyword parameters
    # if you don't have a token already stored on file

    t = oauth_login()

    # Basic usage...

    info = {}
    info.update(get_info_by_screen_name(t, ['ptwobrussell', 'socialwebmining']))
    info.update(get_info_by_id(t, ['2384071']))

    # Do something useful with the profile information like store it to disk

    import json
    print json.dumps(info, indent=1)
