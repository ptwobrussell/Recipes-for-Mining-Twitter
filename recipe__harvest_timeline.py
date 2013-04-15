# -*- coding: utf-8 -*-

import sys
import time
import twitter
import couchdb
from couchdb.design import ViewDefinition
from recipe__oauth_login import oauth_login
from recipe__make_twitter_request import make_twitter_request


def usage():
    print 'Usage: $ %s <timeline name> [max_pages] [user]' % (sys.argv[0], )
    print
    print '\t<timeline name> in [home, user] and is required'
    print '\t0 < max_pages <= 16 for timeline_name in [home, user]'
    print 'Notes:'
    print '\t* ~800 statuses are available from the home timeline.'
    print '\t* ~3200 statuses are available from the user timeline.'
    print '\t* The public timeline must now be accessed with the streaming API.'
    print '\t* See https://dev.twitter.com/docs/api/1.1/get/statuses/sample for details'

    exit()


if len(sys.argv) < 2 or sys.argv[1] not in ('home', 'user'):
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
    'trim_user': 'true',
    'include_rts' : 'true',
    'since_id' : 1,
    }

if TIMELINE_NAME == 'user':
    USER = sys.argv[3]
    KW['screen_name'] = USER
if TIMELINE_NAME == 'home' and MAX_PAGES > 4:
    MAX_PAGES = 4
if TIMELINE_NAME == 'user' and MAX_PAGES > 16:
    MAX_PAGES = 16

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
    # home and user timelines. This is best practice for the Twitter v1.1 API
    # See https://dev.twitter.com/docs/working-with-timelines


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

api_call = getattr(t.statuses, TIMELINE_NAME + '_timeline')
tweets = make_twitter_request(t, api_call, **KW)
db.update(tweets, all_or_nothing=True)
print 'Fetched %i tweets' % len(tweets)

page_num = 1
while page_num < MAX_PAGES and len(tweets) > 0:

    # Necessary for traversing the timeline in Twitter's v1.1 API:
    # Get the next query's max id parameter to pass in.
    # See https://dev.twitter.com/docs/working-with-timelines
    KW['max_id'] = min([ tweet['id'] for tweet in tweets]) - 1 

    api_call = getattr(t.statuses, TIMELINE_NAME + '_timeline')
    tweets = make_twitter_request(t, api_call, **KW)
    
    # Actually storing tweets in CouchDB is as simple as passing them 
    # into a call to db.update

    db.update(tweets, all_or_nothing=True)

    print >> sys.stderr, 'Fetched %i tweets' % (len(tweets),)

    page_num += 1

print >> sys.stderr, 'Done fetching tweets'
