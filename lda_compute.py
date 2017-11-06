import numpy as np
import scipy.sparse
from sklearn.decomposition import LatentDirichletAllocation
import getDataMatrix
import time
import pickle
start_time = time.time()
filename = 'lda_model_apple.pickle'
sparse_matrix, vocab = getDataMatrix.method2('/home/arun/Desktop/sml/Twitter-Stock-Prediction/LDA/export_dashboard_aapl_2016_06_15_14_30_09_Stream.csv')
#sparse_matrix = scipy.sparse.load_npz('apple_sparse_matrix.npz')
print("File Loaded")
n_top_words = 100
lda = LatentDirichletAllocation(n_components=100, max_iter=10,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
print("LDA fitting")
lda.fit(sparse_matrix)
#save pickle
pickle.dump(lda, open(filename, 'wb'))
#load pickle
#lda = pickle.load(open(filename, 'rb'))
x = np.array(lda.components_)
#x = x / x.max(axis=0)
#x = x / x.max(axis=1)
#np.savetxt('test.out', lda.components_, delimiter=',') 
with open('lda_scores_out.txt','a') as f:
	for i, topic_dist in enumerate(x):
		topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
		topic_scores = np.sort(topic_dist)[:-(n_top_words+1):-1]
		topic_strscores = [str(k) for k in topic_scores]
		f.write('Topic {}: {} \n'.format(i, ' '.join(topic_words)))
		f.write('Topic {}: {} \n'.format(i, ' '.join(topic_strscores)))

print("--- %s seconds ---" % (time.time() - start_time))
