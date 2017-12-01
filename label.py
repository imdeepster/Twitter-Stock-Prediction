import csv
import sys
import os

directory_prefix = "data"
temp_dprefix = "temp_LSTM/temp/"
price_prefix = "temp_LSTM/price_temp/"

filenames = os.listdir(directory_prefix)
csv_files = [ filename for filename in filenames if filename.endswith( ".csv" )]


for file in csv_files:
	stock_file = open(directory_prefix+"/"+file, "r",encoding="latin-1")
	stock_file.readline()
	stock_reader = csv.reader(stock_file)

	company = file.split(".")[0].upper()
	# print(company)

	stock_out = open(price_prefix + "/stock_output_with_price_" + company +".csv", "w")
	stock_writer = csv.writer(stock_out, lineterminator='\n')
	stock_writer.writerow(["Id", "Company", "Date", "UnixTS", "Retweets", "Followers", "Sentiments", "Open", "Close"])



	for stock_line in stock_reader:
		#print("Here 1")
		if stock_line:
			#print("Here 2")
			#tweet_file = open("data_matrix.csv", "r")
			if(os.path.isfile(temp_dprefix + "/data_matrix_" + company + ".csv")):
				tweet_file = open(temp_dprefix + "/data_matrix_" + company + ".csv", "r")
				tweet_reader = csv.reader(tweet_file)
				tweet_file.readline()
				for tweet_line in tweet_reader:
					#print(company,tweet_line[1],tweet_line[2],stock_line[0])
					if str(tweet_line[2]) == str(stock_line[0]):
						# print(company, tweet_line[1], tweet_line[2], stock_line[0])
						#print("Here 3")
						tweet_line.append(stock_line[1])
						tweet_line.append(stock_line[4])
						stock_writer.writerow(tweet_line)