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

#df = ticker.irequest('AMD', startDate, endDate)

print(df.tail(20))

#analysis.sma(df, 50)

#analysis.ema(df, 50)

'''
Need to remove NaN from last couple rows of sp-600-index df.
Grab start & end dates from ticker row and plug into irequest().
'''
