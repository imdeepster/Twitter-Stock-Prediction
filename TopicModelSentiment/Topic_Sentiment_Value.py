# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 17:07:37 2017

@author: Bharadwaj
"""

import pandas as pd

df = pd.read_csv('LDA_Topics.csv')
TopicWords = list(doc.split() for doc in df.loc[:, "Words"])

df2 = pd.read_csv('Topic_Sentiment.csv')
TopicSentiment = list(df2.loc[:, "Sentiment"])
TopicSentimentValue = list(df2.loc[:, "SentimentValue"])

dataFrame = pd.read_csv('../DataSet/Apple_True_Data.csv')

tweetdatalist = list(dataFrame.loc[:, "Tweet content"])
tweetSentiment = []
for i in range(0, len(tweetdatalist)):
    words = list(tweetdatalist[i].split())
    sentiment = 0
    for word in words:
        for i in range(0, len(TopicWords)):
            if word in TopicWords[i]:
                if TopicSentiment[i] == "Positive":
                    sentiment += float(TopicSentimentValue[i])
                else:
                    sentiment -= float(TopicSentimentValue[i])
    tweetSentiment.append(sentiment)

print("Done..")