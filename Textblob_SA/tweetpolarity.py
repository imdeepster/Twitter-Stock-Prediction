# -*- coding:utf-8 -*-
import pandas as pd
from textblob import TextBlob
import re
import csv
import numpy as np

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    tweet = re.sub(r"http\S+", "", tweet)
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

categories = ["Highly Negative","Negative","Neutral","Positive","Highly Positive"]
space = np.linspace(-1,1,num=5)

def polarityCompute(cleanedTweet,f):
	polarityOut = TextBlob(cleanedTweet.decode('ascii','ignore'));
	cleanedTweet = cleanedTweet.replace(',',' ').replace(';','').strip()
	cat = categories[np.digitize(polarityOut.sentiment.polarity,space)-1]
	writer = csv.writer(f)
	writer.writerow([cleanedTweet,cat])


fname = "tweetPolarity.csv"
fpath = "../LDA/export_dashboard_msft_2016_06_15_14_35_59_Stream.csv"

filename = fpath.split("/")

dataFrame = pd.read_csv(fpath)
tweetdatalist = list(dataFrame.loc[:, "Tweet content"])
with open(filename[-1], "a") as f:
	size = len(tweetdatalist)
	for i in range(0,size):
		cleanedTweet = clean_tweet(tweetdatalist[i])
		polarityCompute(cleanedTweet,f)
