import pandas as pd
import csv
import os
import math
import  random

price_prefix = "temp_LSTM/price_temp/"
final_prefix = "temp_LSTM/final/"

global_minimum = float("inf")
for file in os.listdir(price_prefix):
    df = pd.read_csv(price_prefix + file)
    group1 = df.groupby(['Date'])
    minimum = group1['Company'].count().min()
    global_minimum = minimum if minimum<global_minimum else global_minimum

print(global_minimum)
past_days = 1
for fi in range(21,101):
    for file in os.listdir(price_prefix):
        df = pd.read_csv(price_prefix + file)
        company = file.split("_")[4]
        stock_final = open(final_prefix + "data_matrix_final_label_"+str(fi)+"_"+company,"w")
        stock_writer = csv.writer(stock_final, lineterminator='\n')

        label_list = []


        div = int(global_minimum/past_days)
        mod = global_minimum%past_days
        #print(div,mod, global_minimum)

        group_dict = {}
        index = 0
        for name, group in df.groupby('Date'):
            group_dict[index] = group.values.tolist()
            index += 1

        for day in list(group_dict.keys())[past_days:]:
            #sample tweets for past n days
            d =1
            temp = []
            for j in range(day-1,day-past_days-1,-1):
                if j == day-1:
                    # tmp = [group_dict[day][i] for i in sorted(random.sample(range(len(group_dict[day])), div+mod))]
                    tmp = [group_dict[j][i] for i in sorted(random.sample(range(len(group_dict[j])), div + mod))]
                else:
                    # tmp = [group_dict[day][i] for i in sorted(random.sample(range(len(group_dict[day])), div))]
                    tmp = [group_dict[j][i] for i in sorted(random.sample(range(len(group_dict[j])), div))]
                for entry in tmp:
                    entry[3] /= d
                    entry[4] /= d
                    entry[5] /= d
                d += 1
                temp += tmp
            #print(len(temp))
            temp_list = []
            for index, row in enumerate(temp):
                if math.isnan(row[5]):
                    row[5] = 0.01
                val = row[3]*row[4]*row[5]*row[6]
                temp_list.append(val)

            # opening_price = group_dict[day - past_days][0][7]
            # closing_price = group_dict[day][0][8]
            opening_price = group_dict[day-past_days][0][7]
            closing_price = group_dict[day][0][7]
            label = 1 if closing_price>opening_price else -1
            #print(opening_price,closing_price,label)
            temp_list += label,
            stock_writer.writerow(temp_list)



