import sys

sys.path.append('C:\PYTHON\lib\site-packages')
from pymongo import Connection
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime


# The MongoDB connection info. This assumes your database name is TwitterStream, and your collection name is tweets.
connection = Connection('localhost', 27017)
db = connection.TwitterStream
db.tweets.ensure_index("id", unique=True, dropDups=True)
collection = db.tweets

# Add the keywords you want to track. They can be cashtags, hashtags, or words.
keywords = ['#MSFT', '$MSFT', '$GOOGL', '#GOOGL', '#pixel2','#googlepixel','#pixel']

#create mapping between keywords and collection names
collectDict = {}
for keys in keywords:
    collection = "db."+str(keys[1:])
    collection = eval(collection)
    collectDict[keys[1:]] = collection

print(collectDict)   

# Optional - Only grab tweets of specific language
language = ['en']

# You need to replace these with your own values that you get after creating an app on Twitter's developer portal.
consumer_key = "53G0Kh8fntJOhOytThh0yVRDk"
consumer_secret = "AuKUly9fZd0Okcbcold1GzNcBkQd4S1AAb16TyLHvfXH4qn9Cg"
access_token = "912761180564754433-e4Vcx5kvcDde6X4eE7hgAY5U4woXyHc"
access_token_secret = "aBr2vnV0Kk5u122Y58TfbhQUrUDuyrYlZZMLysvgHHFxU"

# The below code will get Tweets from the stream and store only the important fields to your database
class StdOutListener(StreamListener):

    def on_data(self, data):

        # Load the Tweet into the variable "t"
        t = json.loads(data)
        # Pull important data from the tweet to store in the database.
        #tweet_id = t['id_str']  # The Tweet ID from Twitter in string format
        username = t['user']['screen_name']  # The username of the Tweet author
        followers = t['user']['followers_count']  # The number of followers the Tweet author has
        text = t['text']  # The entire body of the Tweet
        dt = t['created_at']  # The timestamp of when the Tweet was created

        if 'retweeted_status' in t: 
            retweet_count = len(t['retweeted_status'])

        else:
            retweet_count = 0

       
        if t['is_quote_status']:
            text += ' ' + t['quoted_status']['text']
            
        # Convert the timestamp string given by Twitter to a date object called "created". This is more easily manipulated in MongoDB.
        created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

        # Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
        tweet = {'text':text, 'created':created, 'followers' : followers, 'retweet_count' : retweet_count}

        # Save the refined Tweet data to MongoDB
        #print("text...........", text)
        if not t['retweeted'] and 'RT @' not in t['text']:
            for key in keywords:
                if key in text:
                    print("Adding to database")
                    collection = collectDict[key[1:]]
                    collection.save(tweet)
                
                

        # Optional - Print the username and text of each Tweet to your console in realtime as they are pulled from the stream
        #print(username)
        return True

    # Prints the reason for an error to your console
    def on_error(self, status):
        print(status)

# Some Tweepy code that can be left alone. It pulls from variables at the top of the script
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=keywords, languages=language)
