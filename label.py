import csv
import sys

stock_file = open("data/AAPL.csv", "r",encoding="latin-1")
stock_file.readline()
stock_reader = csv.reader(stock_file)

stock_out = open("stock_output_1.csv","w")
stock_writer = csv.writer(stock_out, lineterminator='\n')

label_list = []
prev_line = stock_file.readline()
for lines in stock_reader:
	tweet_file = open("stock_output.csv","r+")
	tweet_reader = csv.reader(tweet_file)
	
	if lines:
		if(prev_line[4] < lines[4]):
			for stock_line in tweet_reader:
				#print(lines[0] == stock_line[1])
				if lines[0] == stock_line[1]:
					stock_line.append(1)
					stock_writer.writerow(stock_line)
		else:
			for stock_line in tweet_reader:
				if lines[0] == stock_line[1]:
					stock_line.append(-1)
					stock_writer.writerow(stock_line)
		prev_line = lines