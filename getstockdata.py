from pandas_datareader import data
import datetime
import csv
<<<<<<< HEAD
startdate = datetime.datetime(2016,4,2)
enddate = datetime.datetime(2016,6,15)
stocks = ['AAPL','FB', 'GOOGL']
=======
startdate = datetime.datetime(2016,4,1)
enddate = datetime.datetime(2016,6,15)
stocks = ['AAPL','FB', 'GOOGL','MSFT']
>>>>>>> 2b6ee97edbcf2f7509481496d57854c4e0999846
for stock in stocks:
	f = data.DataReader(stock,'yahoo',startdate,enddate)
	f.to_csv(stock+'.csv',mode='a')


