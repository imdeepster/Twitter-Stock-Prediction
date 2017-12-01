import csv
import sys
import os
import glob
import calendar
import time
import datetime

# directory_prefix = "LDA/"
# sent_file_prefix = "Textblob_SA/"
# temp_prefix = "temp/"

directory_prefix = "LDA_LSTM/"
sent_file_prefix = "LSTMSentiment/"
temp_prefix = "temp_LSTM/"

# filenames = os.listdir(directory_prefix)
# csv_files = [ filename for filename in filenames if filename.endswith( ".csv" ) and filename.startswith('export_dashboard')]
#
# filenames = os.listdir(sent_file_prefix)
# sent_files = [ filename for filename in filenames if filename.endswith( ".csv" ) and filename.startswith('export_dashboard')]

filenames = os.listdir(directory_prefix)
csv_files = [ filename for filename in filenames if filename.endswith( ".csv" ) and filename.startswith('export_dashboard')]

filenames = os.listdir(sent_file_prefix)
sent_files = [ filename for filename in filenames if filename.endswith( ".csv" )]

for file in csv_files:

    #tweet_raw_file = open("LDA/export_dashboard_aapl_2016_06_15_14_30_09_Stream.csv", "r",encoding="latin-1")
    tweet_raw_file = open(directory_prefix + "/" + file, "r",encoding="latin-1")
    company = file.split("_")[2].upper()

    stock_out = open(temp_prefix + "/stock_output_"+company+".csv", "w")
    stock_writer = csv.writer(stock_out, lineterminator='\n')
    stock_writer.writerow(["Company","Date","UnixTS","Retweets","Followers","Sentiments"])

    tweet_raw_file.readline()
    tweet_raw_reader = csv.reader(tweet_raw_file)

    tweet_file = open(directory_prefix + "/tweet_file.csv","w")
    tweet_writer = csv.writer(tweet_file, lineterminator='\n')

    sent_list = []

    for lines in tweet_raw_reader:
        if lines != []:
            date = calendar.timegm(time.strptime(lines[1] + " " + lines[2], '%Y-%m-%d %H:%M'))
            # fdate = datetime.datetime.strptime(lines[1], '%Y-%m-%d').strftime('%m-%d-%Y')

            sent_list.append([company,lines[1], date,lines[8] if lines[8] else 0, lines[14] if lines[14] else 0])
            #lines[1] = "/".join(reversed(lines[1].split("-")))

            #print(fdate)
            tweet_writer.writerow([company,lines[1],date, lines[8] if lines[8] else 0, lines[14] if lines[14] else 0])

    #sent_file = open("Textblob_SA/export_dashboard_aapl_2016_06_15_14_30_09_Stream.csv", "r", encoding="latin-1")

    for file in sent_files:
        if company.lower() in file:
            sent_open = file
            break
    sent_file = open(sent_file_prefix + "/" + sent_open ,"r", encoding="latin-1")
    sent_reader = csv.reader(sent_file)

    tweet_file1 = open(directory_prefix + "/tweet_file.csv","r")

    i = 0
    for line in sent_reader:
        sent_list[i].append(line[1])
        i+= 1


    for elem in sent_list:
        stock_writer.writerow(elem)
