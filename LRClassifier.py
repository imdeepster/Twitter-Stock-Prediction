# import numpy as np
# import csv
# from sklearn import linear_model, datasets
# import os
#
# train_prefix = "temp/final/train/"
# test_prefix = "temp/final/test/"
#
#
# # data = open("data_matrix_final_label.csv","r")
# # data_read = csv.reader(data)
#
# input = []
# label = []
# # for lines in data_read:
# #     input.append([float(elem) for elem in lines[0:-1]])
# #     label.append(float(lines[-1]))
# #
# # X = np.array(input)
# # Y = np.array(label)
#
# for file in os.listdir(train_prefix):
#     data = open(train_prefix + file,"r")
#     data_read = csv.reader(data)
#     for lines in data_read:
#         input.append([float(elem) for elem in lines[0:-1]])
#         label.append(float(lines[-1]))
#
# X = np.array(input)
# Y = np.array(label)
#
#
# h = .02  # step size in the mesh
#
# logreg = linear_model.LogisticRegression(C=1e5)
#
# # we create an instance of Neighbours Classifier and fit the data.
# logreg.fit(X, Y)
#
# test_X = []
# test_Y = []
# for file in os.listdir(test_prefix):
#     data = open(test_prefix + file, "r")
#     data_read = csv.reader(data)
#     for lines in data_read:
#         test_X.append([float(elem) for elem in lines[0:-1]])
#         test_Y.append(float(lines[-1]))
#
# test_X = np.array(test_X)
# test_Y = np.array(test_Y)
# i = 0
# count = 0
#
# for elem in test_X:
#     pre = logreg.predict([elem])
#     print(pre, test_Y[i])
#     if pre == test_Y[i]:
#         count +=1
#     i += 1
# print("LR Classifier accuracy:", (count/len(test_Y))*100)
# # i = 0
# # count = 0
# # for elem in X:
# #     pre = logreg.predict([elem])
# #     if pre == Y[i]:
# #         count +=1
# #     i += 1
# #
# # print("LR Classifier accuracy:", count)


import numpy as np
import csv

from sklearn import linear_model, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn import metrics
import os

train_prefix = "temp/final/train_5/"
test_prefix = "temp/final/test/"

input = []
label = []

for file in os.listdir(train_prefix):
    data = open(train_prefix + file,"r")
    data_read = csv.reader(data)
    for lines in data_read:
        input.append([float(elem) for elem in lines[0:-1]])
        label.append(float(lines[-1]))

X = np.array(input)
Y = np.array(label)

h = .02  # step size in the mesh

X_train, X_test, y_train, y_test = train_test_split(X, Y,
                                                    test_size=0.2)
std_clf = make_pipeline(StandardScaler(), linear_model.LogisticRegression(C=1e5))
std_clf.fit(X_train, y_train)
pred_test_std = std_clf.predict(X_test)

print('{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test_std)))