import pandas as pd
import numpy as np
import csv

df = pd.read_csv('LDA_Topics.csv')
TopicWords = list(doc.split() for doc in df.loc[:, "Words"])

df2 = pd.read_csv('Topic_Sentiment.csv')
TopicSentiment = list(df2.loc[:, "Sentiment"])
TopicSentimentValue = list(df2.loc[:, "SentimentValue"])

dataFrame = pd.read_csv('../LDA/export_dashboard_aapl_2016_06_15_14_30_09_Stream.csv')

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
mins = min(tweetSentiment)
maxs = max(tweetSentiment)

categories = ["Very Negative","Negative","Okay","Positive","Very Positive"]
space = np.linspace(-1,1,num=5)

with open("output-sentiment.csv", "a") as f:
    writer = csv.writer(f)
    for i in range(0,len(tweetSentiment)):
        tweetSentiment[i] = categories[np.digitize((2*((tweetSentiment[i] - mins)/(maxs-mins))-1),space)-1]
        writer.writerow([tweetdatalist[i].replace(',',' ').replace(';','').strip(),tweetSentiment[i]])
