#!/usr/bin/env python
from pymongo import Connection
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json
import collections
import types
import time
import datetime
import sys
from pprint import pprint

# ----------------------
# Functions 
# ----------------------
# Read threads
def readThreads(subreddit):
	for t in subreddit:
		
		# Get the thread info
		threadId = t['data']['id']
		title = t['data']['title']
		text = t['data']['selftext']
		permalink = t['data']['permalink']
		score = t['data']['score']
		created = t['data']['created_utc']
		
		redditThread = {'text':title, 'desc':text,'permalink':permalink,'created':created}
		# Save it to the database. Duplicate threads will be ignored due to the UNIQUE KEY constraint
		try:
			collection.save(redditThread)
		except Exception as e:
			print ("Thread not saved")
		print("Thread saved") 
		jsonData = requestJson(baseUrl + urllib2.quote(permalink.encode('utf8')) + ".json", delay)
		postData = jsonData[0]['data']['children']
		readComments(postData, threadId, permalink)
		data = jsonData[1]['data']['children']
		readComments(postData, threadId, permalink)

# Recursive function to read comments
def readComments(obj, threadId, threadUrl):

	for i in obj:

		# Basic info, present both in Title and Comment
		commentId = i['data']['id']
		content = ""
		url = ""
		score = 0
		created = 0
		if 'created_utc' in i['data']:
			created = i['data']['created_utc']
		else:
			print ("Error")

		# Is it a comment?
		if 'body' in i['data']:

			url = threadUrl + commentId
			content = i['data']['body']
			ups = int(i['data']['ups'])
			downs = int(i['data']['downs'])
			score = ups - downs

		# Or is it the title post?
		elif 'selftext' in i['data']:

			url = i['data']['url']
			content = i['data']['selftext']
			score = i['data']['score']

		redditThread = {'text':content,'desc':"", 'permalink':"",'created':created}
		try:
			collection.save(redditThread)
		except Exception as e:
			print ("Thread not saved")
		print("Thread saved") 
		if 'replies' in i['data'] and len(i['data']['replies']) > 0:
			readComments(i['data']['replies']['data']['children'], threadId, threadUrl)

def requestJson(url, delay):
	while True:
		try:
			# Reddit API Rules: "Make no more than thirty requests per minute"
			time.sleep(delay)

			req = urllib2.Request(url, headers=hdr)
			response = urllib2.urlopen(req)
			jsonFile = response.read()
			return json.loads(jsonFile.decode('utf-8'))
		except Exception as e:
			print (e)

# ----------------------
# Script begins here
# ----------------------

# Setup ------------------------------------------

connection = Connection('localhost', 27017)
db = connection.RedditStream
collection = db.reddit
delay = 5
# Url, header and request delay
# If we don't set an unique User Agent, Reddit will limit our requests per hour and eventually block them
userAgent = "Python crypto crawler v1.0 (by /u/ledzepp106)"
if userAgent == "":
	print ("Error: you need to set an User Agent inside this script")
	sys.exit()

hdr = {'User-Agent' : userAgent}
baseUrl = "http://www.reddit.com"

subreddit = "/r/bitcoin"
subredditUrl = baseUrl + subreddit + "/new/.json"

print ("Starting crawler")
print ("Press ctrl+c to stop")


# Start! -----------------------------------------
while True:

	# Log starting time
	startingTime = datetime.datetime.now()
	# Read the Threads
	print ("Requesting new threads...")
	jsonObj = requestJson(subredditUrl, delay)

	# Save the threads
	readThreads(jsonObj['data']['children'])