import numpy as np
import csv
from sklearn.naive_bayes import GaussianNB

data = open("data_matrix_final_label.csv","r")
data_read = csv.reader(data)

input = []
label = []
for lines in data_read:
    input.append([float(elem) for elem in lines[0:-1]])
    label.append(float(lines[-1]))

X = np.array(input)
Y = np.array(label)

clf = GaussianNB()
clf.fit(X,Y)

i = 0
count = 0
for elem in X:
    pre = clf.predict([elem])
    if pre == Y[i]:
        count +=1
    i += 1
print("NB Classifier accuracy:", count)