import numpy as np
import pandas as pd
import tensorflow as tf
import re
from random import randint
import datetime



strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
maxSeqLength = 50 #Maximum length of sentence
numDimensions = 25 #Dimensions for each word vector
path1 = '/home/arun/Desktop/sml/Twitter-Stock-Prediction/Textblob_SA/export_dashboard_googl_2016_06_15_13_06_09_Stream.csv'
path2 = '/home/arun/Desktop/sml/Twitter-Stock-Prediction/Textblob_SA/export_dashboard_aapl_2016_06_15_14_30_09_Stream.csv'
def cleanSentences(string):
    string = string.lower().replace("<br />", " ")
    return re.sub(strip_special_chars, "", string.lower())

#file = open('/media/arun/DATAPART/Arun/school/SML/glove.twitter.27B/glove.twitter.27B.25d.txt','r')
#wordlist = []
#wordvectors = []

#for line in file:
#  listline = line.split()
#  wordlist.append(listline[0])
#  wordvectors.append(np.array(listline[1:]).astype(float))
#np.save('wordlist.npy',wordlist)
#np.save('wordvec.npy',wordvectors)
#print(len(wordlist))
#print(len(wordvectors))

wordsList = np.load('wordlist.npy')
print('Loaded the word list!')
wordsList = wordsList.tolist() #Originally loaded as numpy array
#print(wordsList[:10])
wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8
wordVectors = np.load('wordvec.npy')
print(wordVectors[0][0].dtype)
print ('Loaded the word vectors!')

#baseballIndex = wordsList.index('baseball')
#print(wordVectors[baseballIndex])

dataFrame1 = pd.read_csv(path1)
tweetdatalist = list(dataFrame1.iloc[:, 0])
sentiment1 = list(dataFrame1.iloc[:, 1])

dataFrame2 = pd.read_csv(path2)
sentiment2 = list(dataFrame2.iloc[:,1]) 

sentiment = sentiment1 + sentiment2

print("Sentiment Len")
print(len(sentiment))
# print(len(tweetdatalist))
# print(len(sentiment))
sent_set = list(set(sentiment))
sent_dict = {}
print(sent_set)

for sent in range(len(sent_set)):
  temparr = [0,0,0,0,0]
  temparr[sent] = 1
  print(temparr)
  sent_dict[sent_set[sent]] =  temparr
print(sent_dict)
# numFiles = len(sent_set)
# ids = np.zeros((numFiles, maxSeqLength), dtype='int32')
# fileCounter = 0
# for line in tweetdatalist:
#     indexCounter = 0
#     cleanedLine = cleanSentences(line)
#     split = cleanedLine.split()
#     print(fileCounter)
#     which_sent = sent_dict[sentiment[fileCounter]]
#     for word in split:
# 	try:
#             ids[which_sent][indexCounter] = wordsList.index(word)
#         except ValueError:
#             ids[which_sent][indexCounter] = 399999 #Vector for unknown words
#         indexCounter = indexCounter + 1
#     fileCounter+=1
# np.save('idsMatrix_googl', ids)
# print("SAVED")

ids1 = np.load('idsMatrix_googl.npy')
ids2 = np.load('idsMatrix_apple.npy')
ids = np.concatenate((ids1,ids2),axis=0)
print("loaded",ids.dtype)
print(len(ids))
factor = 150000

batchSize = 24
lstmUnits = 64
numClasses = 5
iterations = 100000

tf.reset_default_graph()

labels = tf.placeholder(tf.float32, [batchSize, numClasses])
input_data = tf.placeholder(tf.int32, [batchSize, maxSeqLength])

data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]),dtype=tf.float32)
data = tf.nn.embedding_lookup(tf.cast(wordVectors, tf.float32),input_data)

lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)
lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.75)
value, _ = tf.nn.dynamic_rnn(lstmCell, data, dtype=tf.float32)

weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
value = tf.transpose(value, [1, 0, 2])
last = tf.gather(value, int(value.get_shape()[0]) - 1)
prediction = (tf.matmul(last, weight) + bias)

correctPred = tf.equal(tf.argmax(prediction,1), tf.argmax(labels,1))
accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float64))

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=labels))
optimizer = tf.train.AdamOptimizer().minimize(loss)


# sess = tf.InteractiveSession()
# saver = tf.train.Saver()
# sess.run(tf.global_variables_initializer())

def getTrainBatch():
    labels = []
    arr = np.zeros([batchSize, maxSeqLength])
    for i in range(batchSize):
        num = randint(1,factor)
        labels.append(list(sent_dict[sentiment[num]]))
        arr[i] = ids[num]
    return arr, labels

def getTestBatch():
    labels = []
    arr = np.zeros([batchSize, maxSeqLength])
    for i in range(batchSize):
        num = randint(factor,len(ids)-1)
        labels.append(sent_dict[sentiment[num]])
        arr[i] = ids[num]
    return arr, labels

# tf.summary.scalar('Loss', loss)
# tf.summary.scalar('Accuracy', accuracy)
# merged = tf.summary.merge_all()
# logdir = "tensorboard/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "/"
# writer = tf.summary.FileWriter(logdir, sess.graph)

# for i in range(iterations):
#    #Next Batch of reviews
#    nextBatch, nextBatchLabels =  getTrainBatch();
#    sess.run(optimizer, {input_data: nextBatch, labels: nextBatchLabels})

#    #Write summary to Tensorboard
#    if (i % 50 == 0):
#        summary = sess.run(merged, {input_data: nextBatch, labels: nextBatchLabels})
#        writer.add_summary(summary, i)

#    #Save the network every 10,000 training iterations
#    if (i % 10000 == 0 and i != 0):
#        save_path = saver.save(sess, "models/pretrained_lstm.ckpt", global_step=i)
#        print("saved to %s" % save_path)
# writer.close()

#=====================================
#           TEST
#=====================================

sess = tf.InteractiveSession()
saver = tf.train.Saver()
#saver = tf.train.import_meta_graph("/home/arun/Desktop/LSTM-Sentiment-Analysis/models/pretrained_lstm.ckpt-90000.meta")
saver.restore(sess, tf.train.latest_checkpoint('models'))
iterations = 40
avg_acc = 0.0
for i in range(iterations):
    nextBatch, nextBatchLabels = getTestBatch();
    avg_acc += (sess.run(accuracy, {input_data: nextBatch, labels: nextBatchLabels})) * 100
    print("Accuracy for this batch:", (sess.run(accuracy, {input_data: nextBatch, labels: nextBatchLabels})) * 100)

print("Average Test Accuracy")
print(avg_acc/iterations)