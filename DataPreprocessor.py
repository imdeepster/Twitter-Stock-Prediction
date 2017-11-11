import pandas as pd

df = pd.read_csv('stock_output.csv')

#For sampling
#print(df.groupby(['date'], as_index=False)['Company'].max())
group1 = df.groupby(['Date']);
print(group1)
min = group1['Company'].min()

#for grouping and normalizing
df_data = []
dic = {'Highly Negative' : -1, 'Negative' : -0.6, 'Neutral' :0.1, 'Positive' : 0.6, 'Highly Positive': 1}

for name, group in df.groupby('Date'):
    group[['Retweets','Followers','UnixTS']] = group[['Retweets','Followers','UnixTS']].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    group[['Retweets', 'Followers', 'UnixTS']] += .01
    group['Sentiments'] = group['Sentiments'].map(dic)
    df_data.append(group)
    # print(group)

result = pd.concat(df_data)
print(result)
# result.drop(result.columns[1], axis=1)
result.to_csv('data_matrix.csv')




#print(group['Company'].min())
#print(df.groupby("date").apply(lambda df:df.irow(df.value.argmax())))
