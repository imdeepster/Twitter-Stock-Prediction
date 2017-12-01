import pandas as pd
import os
temp_prefix = "temp_LSTM/"
temp_dprefix = "temp_LSTM/temp/"
for file in os.listdir(temp_prefix):
    if os.path.isdir(temp_prefix + file):
        continue
    print(file)
    company = file.split("_")[2]
    #df = pd.read_csv('stock_output.csv')
    df = pd.read_csv(file)
    #For sampling
    #print(df.groupby(['date'], as_index=False)['Company'].max())
    group1 = df.groupby(['Date']);

    df['Date'] = pd.to_datetime(df['Date'])
    #print(df)
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
    # result['Date'] = result['Date'].dt.strftime
    # print(result)
    # result.drop(result.columns[1], axis=1)
    result.to_csv(temp_dprefix + '/data_matrix_'+ company )




    #print(group['Company'].min())
    #print(df.groupby("date").apply(lambda df:df.irow(df.value.argmax())))
