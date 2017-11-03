# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 17:47:44 2017

@author: Bharadwaj
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import csv
import re
import string
import math
import numpy as np
from nltk.corpus import stopwords
from datetime import datetime
from scipy.sparse import csr_matrix

dataFrame = pd.read_csv('../DataSet/Apple_True_Data.csv')
#getting date in "%Y-%m-%dT%H:%M:%S.%fZ" format
dataFrame["DateTime"] = dataFrame["Date"].map(str) + 'T'+ dataFrame["Hour"] + ':00.00Z'

tweetdatalist = list(dataFrame.loc[:, "Tweet content"])
tweettimelist = list(dataFrame.loc[:, "DateTime"])
rtlist = list(dataFrame.loc[:, "RTs"])
followerslist = list(dataFrame.loc[:, "Followers"])

stop_words = list(stopwords.words('english'))
translate_table_for_punctuation = dict((ord(char), None) for char in string.punctuation)  

def build_lexicon(corpus):
    lexicon = set()    
    for doc in corpus:
        #removing links
        doc = re.sub(r'http\S+', '', doc)        
        #remove punctuation
        doc = doc.translate(translate_table_for_punctuation)        
        #remove numbers                
        list_of_words_n_doc = doc.split()
        lexicon.update([word for word in list_of_words_n_doc if not word in stop_words])
    return lexicon

vocabularylist = list(build_lexicon(tweetdatalist))
vectorizer = TfidfVectorizer(min_df=1, vocabulary=vocabularylist)
tfidfvector= vectorizer.fit_transform(tweetdatalist)

timenormlist = []
rtnormlist = []
followersnormlist = []
size = len(tweettimelist)
min_tweet_time =  datetime.strptime(min(tweettimelist), "%Y-%m-%dT%H:%M:%S.%fZ")
max_tweet_time =  datetime.strptime(max(tweettimelist), "%Y-%m-%dT%H:%M:%S.%fZ")
range_tweet_time = (max_tweet_time - min_tweet_time).total_seconds()
max_rt = max(rtlist)
max_followers = max(followerslist)

for i in range(0, size):
    time_diff = (datetime.strptime(tweettimelist[i], "%Y-%m-%dT%H:%M:%S.%fZ") - min_tweet_time).total_seconds()
    timenormlist.append(1+(float(time_diff)/range_tweet_time))
    if math.isnan(rtlist[i]):
        rtnormlist.append(1)
    else:
        rtnormlist.append(1+ float(rtlist[i])/float(max_rt))
    if math.isnan(followerslist[i]):
        followersnormlist.append(1)
    else:
        followersnormlist.append(1+float(followerslist[i])/float(max_followers)) 

rows,cols = tfidfvector.nonzero()

for row,col in zip(rows,cols):
    tfidfvector[row,col] = float(tfidfvector[row,col])*timenormlist[row]*rtnormlist[row]*followersnormlist[row]
    
with open("output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(tfidfvector)
    
print("Done..")