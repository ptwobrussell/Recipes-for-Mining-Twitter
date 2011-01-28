# -*- coding: utf-8 -*-

import os
import sys
import webbrowser
import json
from cgi import escape
from math import log
import couchdb
from couchdb.design import ViewDefinition

# Use recipe__harvest_timeline.py to load some data before running
# this script. It loads data from CouchDB, not Twitter's API.

DB = sys.argv[1]

HTML_TEMPLATE = 'etc/tagcloud_template.html'
MIN_FREQUENCY = 2
MIN_FONT_SIZE = 3
MAX_FONT_SIZE = 20

server = couchdb.Server('http://localhost:5984')
db = server[DB]

# Map entities in tweets to the docs that they appear in

def entity_count_mapper(doc):
    if not doc.get('entities'):
        import twitter_text

        def get_entities(tweet):

            # Now extract various entities from it and build up a familiar structure

            extractor = twitter_text.Extractor(tweet['text'])

            # Note that the production Twitter API contains a few additional fields in
            # the entities hash that would require additional API calls to resolve

            entities = {}
            entities['user_mentions'] = []
            for um in extractor.extract_mentioned_screen_names_with_indices():
                entities['user_mentions'].append(um)

            entities['hashtags'] = []
            for ht in extractor.extract_hashtags_with_indices():

                # massage field name to match production twitter api

                ht['text'] = ht['hashtag']
                del ht['hashtag']
                entities['hashtags'].append(ht)

            entities['urls'] = []
            for url in extractor.extract_urls_with_indices():
                entities['urls'].append(url)

            return entities

        doc['entities'] = get_entities(doc)

    # A mapper can, and often does, include multiple calls to "yield" which 
    # emits a key, value tuple. This tuple can be whatever you'd like. Here,
    # we emit a tweet entity as the key and the tweet id as the value, even
    # though it's really only the key that we're interested in analyzing.

    if doc['entities'].get('user_mentions'):
        for user_mention in doc['entities']['user_mentions']:
            yield ('@' + user_mention['screen_name'].lower(), doc['id'])

    if doc['entities'].get('hashtags'):
        for hashtag in doc['entities']['hashtags']:
            yield ('#' + hashtag['text'], doc['id'])


# Count the frequencies of each entity

def summing_reducer(keys, values, rereduce):
    if rereduce:
        return sum(values)
    else:
        return len(values)


# Creating a "view" in a "design document" is the mechanism that you use
# to setup your map/reduce query

view = ViewDefinition('index', 'entity_count_by_doc', entity_count_mapper,
                      reduce_fun=summing_reducer, language='python')

view.sync(db)

entities_freqs = [(row.key, row.value) for row in
                  db.view('index/entity_count_by_doc', group=True)]

# Create output for the WP-Cumulus tag cloud and sort terms by freq along the way

raw_output = sorted([[escape(term), '', freq] for (term, freq) in entities_freqs
                    if freq > MIN_FREQUENCY], key=lambda x: x[2])

# Implementation details for the size of terms in the tag cloud were adapted from 
# http://help.com/post/383276-anyone-knows-the-formula-for-font-s

min_freq = raw_output[0][2]
max_freq = raw_output[-1][2]


def weightTermByFreq(f):
    return (f - min_freq) * (MAX_FONT_SIZE - MIN_FONT_SIZE) / (max_freq
            - min_freq) + MIN_FONT_SIZE


weighted_output = [[i[0], i[1], weightTermByFreq(i[2])] for i in raw_output]

# Substitute the JSON data structure into the template

html_page = open(HTML_TEMPLATE).read() % \
                 (json.dumps(weighted_output),)

if not os.path.isdir('out'):
    os.mkdir('out')

f = open(os.path.join(os.getcwd(), 'out', os.path.basename(HTML_TEMPLATE)), 'w')
f.write(html_page)
f.close()

print >> sys.stderr, 'Tagcloud stored in: %s' % f.name

# Open up the web page in your browser

webbrowser.open("file://" + f.name)
