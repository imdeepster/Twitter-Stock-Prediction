import pandas as pd
import csv

df = pd.read_csv('stock_output_1.csv')

stock_final = open("data_matrix_final_label.csv","w")
stock_writer = csv.writer(stock_final, lineterminator='\n')

group1 = df.groupby(['Date'])
minimum = group1['Company'].count().min()
#print(minimum)
output_list = []
label_list = []
for name, group in df.groupby('Date'):
    temp = group.sample(minimum)
    #print(temp)
    temp_list = []
    for index,row in temp.iterrows():
        temp_list.append(row[2]*row[3]*row[4]*row[5])
    output_list.append(temp_list)
    label_list.append(temp.iloc[0]['Label'])
    temp_list.append(temp.iloc[0]['Label'])
    stock_writer.writerow(temp_list)



# print(len(output_list))
# # for elem in output_list:
# #     print(elem)
# print(len(label_list),label_list)

