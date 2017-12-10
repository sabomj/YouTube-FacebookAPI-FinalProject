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
from datetime import datetime
import plotly
plotly.tools.set_credentials_file(username='madijsabo', api_key='B418Xy5P1C5nRnWcZBzx')
import plotly.plotly as py
import plotly.graph_objs as go



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

lst =[]
mon =[]
tue = []
wed = []
thurs = []
fri =[]
sat = []
sun =[]
br = [0,0,0,0,0,0,0]
for plot in database['data']:
    x = datetime.strptime(plot['created_time'],"%Y-%m-%dT%H:%M:%S%z")
    data = (datetime.strftime(x, "%A:%H"))
    lst.append(data)

    if 'Mon' in data:
        br[0]+= 1
    if 'Tue' in data:
        br[1]+= 1
    if 'Wed' in data:
        br[2]+= 1
    if 'Thurs' in data:
        br[3]+= 1
    if 'Fri' in data:
        br[4]+= 1
    if 'Sat' in data:
        br[5]+= 1
    if 'Sun' in data:
        br[6]+= 1

print (br)




conn = sqlite3.connect('sabofinalproject.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Posts')
cur.execute('CREATE TABLE Posts (message TEXT, created_time DATETIME)')

for post_time in database['data']:
    x = datetime.strptime(post_time['created_time'],"%Y-%m-%dT%H:%M:%S%z")
    data = (post_time['message'], datetime.strftime(x, "%A:%H"))
    cur.execute('INSERT or IGNORE INTO Posts VALUES (?,?)', data)

conn.commit()




#
data = [go.Bar(
            x=['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday'],
            y= br
    )]

py.plot(data, filename='basic-bar')

#-------------------------------------------------------------------------------

# def get_OMDBdata(name):
# 	baseurl = "http://www.omdbapi.com/?"
#
# 	if name in CACHE_DICTION:
# 		print('using cache')
# 		response_text = CACHE_DICTION[name]
#
# 	else:
# 		print('fetching')
# 		omdb = requests.get(baseurl, params = {"t":name, "type":"movie"}).text
# 		omdb_return = json.loads(omdb)
# 		CACHE_DICTION[name] = omdb_return
# 		response_text = omdb_return
# 		cache_file = open(CACHE_FNAME, 'w')
# 		cache_file.write(json.dumps(CACHE_DICTION))
# 		cache_file.close()
#
# 	return response_text
#
# hello = get_OMDBdata('Pretty Woman')
