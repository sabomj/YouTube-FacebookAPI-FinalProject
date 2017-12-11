#Madeleine Sabo
#SI206
#PROJECTFINALfacebook

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
import omdb

#token in file facebook_token.py
fb_token = facebook_token.fb_token
CACHE_FNAME = 'fb.json'

try:
    cache_file: open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

#try to see if search is in cache, if not then caches
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

fdatabase = get_user_post_time(fb_page)
#calls get_user_post_time and creates the json file of stranger things fb page posts


conn = sqlite3.connect('fb.sqlite')
cur = conn.cursor()

#creates table "posts"
cur.execute('DROP TABLE IF EXISTS Posts')
cur.execute('CREATE TABLE Posts (message TEXT, created_time DATETIME)')

for post_time in fdatabase['data']:#reiterating through the data created from calling graph API
    x = datetime.strptime(post_time['created_time'],"%Y-%m-%dT%H:%M:%S%z") #turns unix time from facebook into Day of the week
    data = (post_time['message'], datetime.strftime(x, "%A:%H")) #creates data with post title and time of post but in the form Day:Hour
    cur.execute('INSERT or IGNORE INTO Posts VALUES (?,?)', data) #puts data into the database

conn.commit()


facebook_days = [0,0,0,0,0,0,0] #each 0 for every day of the week mon-sun
for plot in fdatabase['data']:
    x = datetime.strptime(plot['created_time'],"%Y-%m-%dT%H:%M:%S%z")
    data = (datetime.strftime(x, "%A:%H"))
#will go through the data and add the list facebook_days depending on the day
    if 'Mon' in data:
        facebook_days[0]+= 1
    if 'Tue' in data:
        facebook_days[1]+= 1
    if 'Wed' in data:
        facebook_days[2]+= 1
    if 'Thurs' in data:
        facebook_days[3]+= 1
    if 'Fri' in data:
        facebook_days[4]+= 1
    if 'Sat' in data:
        facebook_days[5]+= 1
    if 'Sun' in data:
        facebook_days[6]+= 1

# print (facebook_days)


print('Creating Plotly for Stranger Things Facebook Page Posts')
#plotly bar chart code
trace = go.Bar(
    x=['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday'],
    y= facebook_days, #takes the list of numbers from facebook_days and matches with monday-sunday
)

layout = go.Layout(
    title='Last 100 Posts From The Stranger Things Facebook Page',
    xaxis=dict(
        title='Day of the Week'

    ),
    yaxis=dict(
        title='Amount of Posts',

        )
    )


data = [trace]
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='style-bar') #creates plot
