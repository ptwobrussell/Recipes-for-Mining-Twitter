# -*- coding: utf-8 -*-

from recipe__make_twitter_request import make_twitter_request

# XXX: TEST ME

# Assume ids have been fetched from a scenario such as the
# one presented in recipe__get_friends_followers.py and that
# t is an authenticated instance of twitter.Twitter

def getInfoById(t, ids):

    id_to_info = {}

    while len(ids) > 0:

        # Process 100 ids at a time...

        ids_str, ids = ','.join([str(_id) for _id in ids[:100]])
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

def getInfoByScreenName(t, screen_names):

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
