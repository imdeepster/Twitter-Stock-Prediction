import numpy as np
import csv
import os
from sklearn.naive_bayes import GaussianNB

train_prefix = "temp/final/train/"
test_prefix = "temp/final/test/"

input = []
label = []

for file in os.listdir(test_prefix):
    data = open(test_prefix + file,"r")
    data_read = csv.reader(data)
    for lines in data_read:
        input.append([float(elem) for elem in lines[0:-1]])
        label.append(float(lines[-1]))

X = np.array(input)
Y = np.array(label)

clf = GaussianNB()
clf.fit(X,Y)

test_X = []
test_Y = []
for file in os.listdir(test_prefix):
    data = open(test_prefix + file, "r")
    data_read = csv.reader(data)
    for lines in data_read:
        test_X.append([float(elem) for elem in lines[0:-1]])
        test_Y.append(float(lines[-1]))

test_X = np.array(test_X)
test_Y = np.array(test_Y)
i = 0
count = 0
for elem in test_X:
    pre = clf.predict([elem])
    if pre == test_Y[i]:
        count +=1
    i += 1
print("NB Classifier accuracy:", count, len(test_Y))