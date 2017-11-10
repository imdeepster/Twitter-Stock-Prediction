import csv
import sys

tweet_raw_file = open("LDA/export_dashboard_aapl_2016_06_15_14_30_09_Stream.csv", "r",encoding="latin-1")
tweet_raw_file.readline()
tweet_raw_reader = csv.reader(tweet_raw_file)

tweet_file = open("LDA/apple_tweet_file.csv","w")
tweet_writer = csv.writer(tweet_file, lineterminator='\n')

sent_list = []

for lines in tweet_raw_reader:
    if lines != []:
         sent_list.append(["AAPL",lines[1].strip(), lines[8].strip() if lines[8] else 0, lines[14].strip()])
         tweet_writer.writerow(["AAPL",lines[1].strip(), lines[8].strip() if lines[8] else 0, lines[14].strip()])

sent_file = open("Textblob_SA/export_dashboard_aapl_2016_06_15_14_30_09_Stream.csv", "r", encoding="latin-1")
sent_reader = csv.reader(sent_file)

tweet_file1 = open("LDA/apple_tweet_file.csv","r")

i = 0
for line in sent_reader:
    sent_list[i].append(line[1])
    i+= 1

stock_out = open("stock_output.csv","w")
stock_writer = csv.writer(stock_out, lineterminator='\n')
for elem in sent_list:
    stock_writer.writerow(elem)




