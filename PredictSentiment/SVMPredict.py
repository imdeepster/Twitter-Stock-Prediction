from sklearn.svm import LinearSVC
import numpy as np
import scipy.sparse
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.multiclass import OneVsRestClassifier

matrix = scipy.sparse.load_npz("../apple_sparse_matrix.npz")
classfname = "../Textblob_SA/export_dashboard_aapl_2016_06_15_14_30_09_Stream.csv"
classmatrix = pd.read_csv(classfname,delimiter=',',header=None,encoding='latin-1')
classmatrix = classmatrix.as_matrix(columns=[1])
classmatrix = [val for sublist in classmatrix for val in sublist]
classif = OneVsRestClassifier(LinearSVC().fit(matrix,classmatrix))
scores = cross_val_score(classif, matrix, classmatrix, cv=10)
print("Accuracy: %0.4f" % (scores.mean()))
