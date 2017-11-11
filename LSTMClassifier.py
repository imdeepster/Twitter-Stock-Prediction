import numpy as np
import csv
from sklearn.neural_network import MLPClassifier

data = open("data_matrix_final_label.csv","r")
data_read = csv.reader(data)

input = []
label = []
for lines in data_read:
    input.append([float(elem) for elem in lines[0:-1]])
    label.append(float(lines[-1]))

X = np.array(input)
Y = np.array(label)
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5,3), random_state=1)

clf.fit(X, Y)

i = 0
count = 0
for elem in X:
    pre = clf.predict([elem])
    if pre == Y[i]:
        count +=1
    i += 1

print("LSTM Classifier accuracy:", count)
