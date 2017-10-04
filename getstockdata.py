from pandas_datareader import data
import datetime
import csv
startdate = datetime.datetime(2017,9,1)
enddate = datetime.datetime(2017,10,1)
stocks = ['AAPL','FB', 'GOOGL']
for stock in stocks:
	f = data.DataReader(stock,'yahoo',startdate,enddate)
	f.to_csv(stock+'.csv',mode='a')
