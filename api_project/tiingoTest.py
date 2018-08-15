
from modules import ticker
from modules import analysis
#from modules import chart
from modules import indicator
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt

def simple_line(df, view = 1095):
    if (type(view) == int and view >= 1):
        plot_df = df.tail(view)
        i = plot_df.plot(grid=True)
    else:
        raise ValueError('"view=" needs to be int in days.')
    
    return i

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


analysis.eval_RSI(df, 14)


#weekly_df = analysis.eval_group(df, group='week')
#print(weekly_df.tail(4))
#monthly_df = analysis.eval_group(df, group='month')
#print(monthly_df.tail(4))
#quarterly_df = analysis.eval_group(df, group='quarter')
#print(quarterly_df.tail(4))
#yearly_df = analysis.eval_group(df, group='year')
#print(yearly_df.tail(4))
#
#period = 50
#sm = 'MA' + str(period)
#ema = 'EMA' + str(period)

#indicator.sma(df, 50)
#indicator.sma(df, 90)

#indicator.ema(df, 50)
#indicator.ema(df, 90)

#indicator.RSI(df, 14)
#indicator.eRSI(df, 14)

#graph_df = pd.DataFrame({
#                       'adjClose': df['adjClose'],
#                       'sma': df[sm],
#                       'ema': df[ema],
#                       })

#chart.simple_line(df, view=1095)
#simple_line(graph_df, view=250)

#indicator.macd(df)

#indicator.bollinger_bands(df, 20)

#indicator.mfi(df, 14)

#indicator.chaikin_oscillator(df, 3, 10)
#indicator.chaikin_oscillator(df, 6, 20)
'''
Need to add something to skip running all the calculations
if they have already been done.
'''
#indicator.stochastic_oscillator(df, 14, 3, indicator='Slow')
#indicator.stochastic_oscillator(df, 14, 3, indicator='Fast')

#chart.candlestick(df, stick="day")

#print(df.tail(10))




    
'''

Grab start & end dates from ticker row and plug into irequest().
'''
