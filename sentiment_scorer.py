from nltk.stem import PorterStemmer

port = PorterStemmer()

def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]


fname = "lda_method2_100.100.txt"
with open(fname) as f:
    content = f.readlines()

content = [x.strip() for x in content] 

count = 0
all_dicts = []
words = []
scores = []
for line in content:
  splits = line.split(":")
  which_group = splits[0]
  if count%2 == 0:
    words = splits[1].split()
  else:
    scores = splits[1].split()
    score_dict = {}
    for i in range(len(words)):
      if float(scores[i])>0.01:
        score_dict[words[i]] = scores[i]
      else:
	break
    all_dicts.append(score_dict)
  count+=1  

positive_words = [port.stem(word.decode('utf-8')) for word in read_words('positive-words.txt')]
negative_words = [port.stem(word.strip().decode('utf-8')) for word in read_words('negative-words.txt')]
topic_scores = []
for score_dict in all_dicts:
  score_list = [0.0,0.0]
  for k,v in score_dict.items():
    if k in positive_words:
	score_list[0]+=float(v)
    if k in negative_words:
	score_list[1]+=float(v)
  topic_scores.append(score_list)

for i in range(len(topic_scores)):
  print("Topic: "+ str(i))
  print(all_dicts[i].keys())
  print(topic_scores[i])
  if(topic_scores[i][0]>topic_scores[i][1]):
	percentage = topic_scores[i][0]/float(topic_scores[i][0]+topic_scores[i][1])
        print("Positive: "+ str(percentage))
  if(topic_scores[i][0]<topic_scores[i][1]):
	percentage = topic_scores[i][1]/float(topic_scores[i][0]+topic_scores[i][1])
        print("Negative: "+ str(percentage))  

