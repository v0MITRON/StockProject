import ticker
import analysis
import pandas as pd
import datetime

startDate = datetime.date(2015, 1, 2)
endDate = datetime.date.today()

#ticker.lib()

file = '/home/matt/Projects/Stock Project/API_project/api_project/stockDB.h5'

df = pd.read_hdf(file, '/lib/supported_tickers')
sp600df = ticker.indexupdate('sp-600')

df = df.merge(sp600df, on='ticker', how='right')
df.dropna(subset=['startDate', 'endDate'], inplace=True)


for index, row in df.iterrows():
    ticker = row['ticker']
    startDate = row['startDate']
    endDate = row['endDate']
    
    print(ticker + ', ' + startDate + ', ' + endDate)
    
#df = ticker.irequest('AMD', startDate, endDate)

#print(df.tail(20))

#analysis.sma(df, 50)

#analysis.ema(df, 50)

'''

Grab start & end dates from ticker row and plug into irequest().
'''
