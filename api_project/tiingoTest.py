import ticker
import analysis
import chart
import pandas as pd
import datetime
import time

startDate = datetime.date(2000, 1, 2)
endDate = datetime.date.today()

symbol = 'DNR'
keypath = '/history/' + symbol
#store = pd.HDFStore('stockDB.h5', complevel=9, complib='zlib')
#df = ticker.irequest(symbol, startDate, endDate)
#df.to_hdf(store, key=keypath, format='table', append=True)
#store.close()

file = '/home/matt/Projects/StockProject/API_Project/stockDB.h5'
df = symbol

df = pd.read_hdf(file, keypath)

analysis.sma(df, 50)
#analysis.sma(df, 90)

analysis.ema(df, 50)
#analysis.ema(df, 90)

analysis.rsi(df, 14)

chart.simple_line(df)

chart.candlestick(df, stick="day")

print(df.tail(10))
    
'''

Grab start & end dates from ticker row and plug into irequest().
'''
