#Madeleine Sabo
#SI206
#PROJECTFINAL

import unittest
import itertools
import collections
import sqlite3
import json
import facebook
import requests
import facebook_token

fb_token = facebook_token.fb_token
CACHE_FNAME = 'sabofinalproject.json'

try:
    cache_file: open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

fb_page = 'StrangerThingsTV'
def get_user_post_time(post):
    graph = facebook.GraphAPI(fb_token)
    posts = graph.request(fb_page+'/posts?limit=100')
    if post in CACHE_DICTION:
        print('fetching')
        return CACHE_DICTION[post]
    else:
        print('caching')
        results = posts
        CACHE_DICTION[post] = results
        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION, indent = 2))
        f.close()
    return posts

database = get_user_post_time(fb_page)



conn = sqlite3.connect('sabofinalproject.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Posts')
cur.execute('CREATE TABLE Posts (message TEXT, created_time DATETIME)')

for post_time in database['data']:
    data = (post_time['message'], post_time['created_time'])
    cur.execute('INSERT or IGNORE INTO Posts VALUES (?,?)', data)

conn.commit()
