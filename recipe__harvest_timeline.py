# -*- coding: utf-8 -*-

import sys
import time
import twitter
import couchdb
from couchdb.design import ViewDefinition
from recipe__oauth_login import oauth_login
from recipe__make_twitter_request import make_twitter_request


def usage():
    print 'Usage: $ %s timeline_name [max_pages] [screen_name]' % (sys.argv[0], )
    print
    print '\ttimeline_name in [public, home, user]'
    print '\t0 < max_pages <= 16 for timeline_name in [home, user]'
    print '\tmax_pages == 1 for timeline_name == public'
    print 'Notes:'
    print '\t* ~800 statuses are available from the home timeline.'
    print '\t* ~3200 statuses are available from the user timeline.'
    print '\t* The public timeline updates every 60 secs and returns 20 statuses.'
    print '\t* See the streaming/search API for additional options to harvest tweets.'

    exit()


if len(sys.argv) < 2 or sys.argv[1] not in ('public', 'home', 'user'):
    usage()
if len(sys.argv) > 2 and not sys.argv[2].isdigit():
    usage()
if len(sys.argv) > 3 and sys.argv[1] != 'user':
    usage()

TIMELINE_NAME = sys.argv[1]
MAX_PAGES = int(sys.argv[2])

USER = None

KW = {  # For the Twitter API call
    'count': 200,
    'skip_users': 'true',
    'include_entities': 'true',
    'since_id': 1,
    }

if TIMELINE_NAME == 'user':
    USER = sys.argv[3]
    KW['screen_name'] = USER
if TIMELINE_NAME == 'home' and MAX_PAGES > 4:
    MAX_PAGES = 4
if TIMELINE_NAME == 'user' and MAX_PAGES > 16:
    MAX_PAGES = 16
if TIMELINE_NAME == 'public':
    MAX_PAGES = 1

# Authentication is needed for harvesting home timelines.
# Don't forget to add keyword parameters to the oauth_login call below
# if you don't have a token file on disk.

t = oauth_login()

# Establish a connection to a CouchDB database

server = couchdb.Server('http://localhost:5984')
DB = 'tweets-%s-timeline' % (TIMELINE_NAME, )

if USER:
    DB = '%s-%s' % (DB, USER)

try:
    db = server.create(DB)
except couchdb.http.PreconditionFailed, e:

    # Already exists, so append to it, keeping in mind that duplicates could occur

    db = server[DB]

    # Try to avoid appending duplicate data into the system by only retrieving tweets 
    # newer than the ones already in the system. A trivial mapper/reducer combination 
    # allows us to pull out the max tweet id which guards against duplicates for the 
    # home and user timelines. It has no effect for the public timeline


    # For each tweet, emit tuples that can be passed into a reducer to find the maximum
    # tweet value. 

    def id_mapper(doc):
        yield (None, doc['id'])


    # Find the maximum tweet id
    def max_finding_reducer(keys, values, rereduce):
        return max(values)


    view = ViewDefinition('index', 'max_tweet_id', id_mapper, max_finding_reducer,
                          language='python')
    view.sync(db)
    try:
        KW['since_id'] = int([_id for _id in db.view('index/max_tweet_id')][0].value)
    except IndexError, e:
        KW['since_id'] = 1

# Harvest tweets for the given timeline.
# For friend and home timelines, the unofficial limitation is about 800 statuses 
# although other documentation may state otherwise. The public timeline only returns
# 20 statuses and gets updated every 60 seconds, so consider using the streaming API 
# for public statuses. See http://bit.ly/fgJrAx
# Note that the count and since_id params have no effect for the public timeline

page_num = 1
while page_num <= MAX_PAGES:
    KW['page'] = page_num
    api_call = getattr(t.statuses, TIMELINE_NAME + '_timeline')
    tweets = make_twitter_request(t, api_call, **KW)
    
    # Actually storing tweets in CouchDB is as simple as passing them 
    # into a call to db.update

    db.update(tweets, all_or_nothing=True)

    print >> sys.stderr, 'Fetched %i tweets' % (len(tweets),)

    page_num += 1

print >> sys.stderr, 'Done fetching tweets'
