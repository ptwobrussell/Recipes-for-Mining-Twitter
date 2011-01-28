# -*- coding: utf-8 -*-

import json
import twitter_text

def get_entities(tweet):

    extractor = twitter_text.Extractor(tweet['text'])

    # Note: the production Twitter API contains a few additional fields in
    # the entities hash that would require additional API calls to resolve
    # See API resources that offer the include_entities parameter for details.

    entities = {}
    entities['user_mentions'] = []
    for um in extractor.extract_mentioned_screen_names_with_indices():
        entities['user_mentions'].append(um)

    entities['hashtags'] = []
    for ht in extractor.extract_hashtags_with_indices():

        # Massage field name to match production twitter api

        ht['text'] = ht['hashtag']
        del ht['hashtag']
        entities['hashtags'].append(ht)

    entities['urls'] = []
    for url in extractor.extract_urls_with_indices():
        entities['urls'].append(url)

    return entities

if __name__ == '__main__':

    # A mocked up array of tweets for purposes of illustration.
    # Assume tweets have been fetched from the /search resource or elsewhere.

    tweets = \
        [
           {
            'text' : 'Get @SocialWebMining example code at http://bit.ly/biais2 #w00t'

            # ... more tweet fields ...

           },
           
           # ... more tweets ...

        ]

    for tweet in tweets:
        tweet['entities'] = get_entities(tweet)

    print json.dumps(tweets, indent=1)
