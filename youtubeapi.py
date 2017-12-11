
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import unittest
import itertools
import collections
import sqlite3
import json
import requests
from datetime import datetime
import plotly
import youtubetoken
plotly.tools.set_credentials_file(username='madijsabo', api_key='B418Xy5P1C5nRnWcZBzx')
import plotly.plotly as py
import plotly.graph_objs as go



CACHE_FNAME = 'youtube.json'

try:
    cache_file: open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}


DEVELOPER_KEY = youtubetoken.developer_key #token in file youtubetoken.py
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY) #builds a search request
    response = youtube.search().list(
        q = query, #search term
        part = "snippet",
        maxResults = 50, #maxresults for youtube was only 50, couldn't get 100
        type = "youtube" #only returns videos that have a YouTube License
    ).execute()
    #try to see if search is in cache, if not then caches
    if query in CACHE_DICTION:
        print('fetching')
        return CACHE_DICTION[query]
    else:
        print('caching')
        results = response
        CACHE_DICTION[query] = results
        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION, indent = 2))
        f.close()
    return response

ydatabase = youtube_search('strangerthings')
#calls youtube_search and creates json file with info on videos containing stranger things
conn = sqlite3.connect('youtube.sqlite')
cur = conn.cursor()

#creates table "posts"
cur.execute('DROP TABLE IF EXISTS Posts')
cur.execute('CREATE TABLE Posts (title TEXT, publishedAt DATETIME)') #with title as text and created time as datetime

for post_time in ydatabase['items']:

    x = datetime.strptime(post_time['snippet']['publishedAt'][:-1],"%Y-%m-%dT%H:%M:%S.%f") #turns youtube unix time into year-month-day-minute-second
    data = (post_time['snippet']['title'], datetime.strftime(x, "%A:%H")) #creates data with title of video and published time in form Day:Hour
    cur.execute('INSERT or IGNORE INTO Posts VALUES (?,?)', data) #puts data into database

conn.commit()


youtube_days = [0,0,0,0,0,0,0] #each 0 for every day of the week mon-sun
for plot in ydatabase['items']:
    x = datetime.strptime(plot['snippet']['publishedAt'][:-1],"%Y-%m-%dT%H:%M:%S.%f")
    data = (datetime.strftime(x, "%A:%H"))

#will go through the data and add the list facebook_days depending on the day (0-6, Mon-Sun)

    if 'Mon' in data:
        youtube_days[0]+= 1
    if 'Tue' in data:
        youtube_days[1]+= 1
    if 'Wed' in data:
        youtube_days[2]+= 1
    if 'Thurs' in data:
        youtube_days[3]+= 1
    if 'Fri' in data:
        youtube_days[4]+= 1
    if 'Sat' in data:
        youtube_days[5]+= 1
    if 'Sun' in data:
        youtube_days[6]+= 1

# print (youtube_days)

print('Creating Plotly For YouTube Video Posts Containing Stranger Things')
#plotly bar chart code

trace1 = go.Scatter(
    x=['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday'],
    y=youtube_days, #takes the list of numbers from facebook_days and matches with monday-sunday
    mode='markers',
    name='posts',
    marker=dict(
        color='red',
        line=dict(
            color='magenta',
            width=1.8,
        ),
        symbol='square',
        size=16,
    )
)

layout = go.Layout(
    title='Last 50 YouTube Posts Containing Stranger Things',
    xaxis=dict(
        title='Day of the Week'
    ),
    yaxis=dict(
        title='Amount of Posts',

        )
    )

data = [trace1]
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='style-bar')




trace0 = go.Scatter(
    x=['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday'],
    y=youtube_days,
    mode='markers',
    name='posts',
    marker=dict(
        color='red',
        line=dict(
            color='magenta',
            width=1.5,
        ),
        symbol='square',
        size=16,
    )
)


data = [trace0]
layout = go.Layout(
    title="Last 50 YouTube Posts Containing Stranger Things",
    xaxis=dict(
        title='Day of the Week',
    ),


    yaxis=dict(
        title='Amount of Posts',
    ),


    width=800,
    height=600,
    plot_bgcolor='rgb(253, 238, 252)'

)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='scatterplot')
