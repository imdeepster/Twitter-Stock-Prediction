from pandas_datareader import data
import datetime
import csv
startdate = datetime.datetime(2016,3,29)
enddate = datetime.datetime(2016,6,15)
stocks = ['AMZN']
for stock in stocks:
	f = data.DataReader(stock,'yahoo',startdate,enddate)
	f.to_csv(stock+'.csv',mode='a')


