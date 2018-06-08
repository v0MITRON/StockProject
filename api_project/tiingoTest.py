import ticker
import analysis
import pandas as pd
import datetime

startDate = datetime.date(2015, 1, 2)
endDate = datetime.date.today()

#ticker.lib()

#file = '/home/matt/Projects/Stock Project/API_project/api_project/stockDB.h5'

#table = pd.read_hdf(file, '/lib/supported_tickers')

df = ticker.irequest('AMD', startDate, endDate)

print(df.tail(20))

#analysis.sma(df, 50)

analysis.ema(df, 50)

print(df.tail(20))
