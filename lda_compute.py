import numpy as np
import scipy.sparse
from sklearn.decomposition import LatentDirichletAllocation
import getDataMatrix
import time
start_time = time.time()

sparse_matrix, vocab = getDataMatrix.main('/home/deepak/Downloads/StockPredict/LDA/export_dashboard_aapl_2016_06_15_14_30_09_Stream.csv')
#sparse_matrix = scipy.sparse.load_npz('apple_sparse_matrix.npz')
print("File Loaded")
n_top_words = 100
lda = LatentDirichletAllocation(n_components=100, max_iter=10,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
print("LDA fitting")
lda.fit(sparse_matrix)
#np.savetxt('test.out', lda.components_, delimiter=',') 
with open('ldaout.txt','a') as f:
	for i, topic_dist in enumerate(lda.components_):
		topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
		f.write('Topic {}: {} \n'.format(i, ' '.join(topic_words)))

print("--- %s seconds ---" % (time.time() - start_time))
