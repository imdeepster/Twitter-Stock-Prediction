import numpy as np
from sklearn.decomposition import LatentDirichletAllocation

fname = 'output.csv'
matrix = np.genfromtxt(fname,delimiter=',')
n_top_words = 10
lda = LatentDirichletAllocation(n_components=20, max_iter=10,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda.fit(matrix)
#np.savetxt('test.out', lda.components_, delimiter=',') 
for index, i in enumerate(lda.components_):
	print("\n"+str(index) + " " + str(i))
	for j in i.argsort()[:-n_top_words-1:-1]:
		print(j)
