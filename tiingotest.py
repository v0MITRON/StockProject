#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 21:49:35 2018

@author: matt

Tiingo Auth Token: e03a22d17056b77d1938b28fabfeea3f668a617a
"""

from urllib.request import urlopen, Request
import pandas as pd
import datetime
import time
from tables import *
import h5py
import numpy as np


start = datetime.date(2008, 1, 1)
end = datetime.date.today()

# Get CSV of all companies traded on exchange.
exchange = 'nyse'
url = 'https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=' + exchange + '&render=download'
req = Request(url)

with urlopen(req) as testfile, open('companyinfo.csv', 'w') as f:
    f.write(testfile.read().decode())
    
companyinfo = pd.read_csv('companyinfo.csv')

# Create seperate df with desired info for JSON metadata.
selCompanyInfo = companyinfo[['Symbol', 'Sector', 'industry']]

# Short df for test purposes.  Remove and use 'selCompanyInfo' for full exchange list.
testdf = selCompanyInfo.head(5)
print(testdf)

u1 = "https://api.tiingo.com/tiingo/daily/"
u2 = "/prices?startDate="
u3 = "&endDate="
token = "&token=e03a22d17056b77d1938b28fabfeea3f668a617a"


# Open/create HDF5 file using pandas
#store = pd.HDFStore('stockData.h5')



# Iterate down df pulling stock symbol for history download
stockindex = 0
while stockindex < 5:
    stock = testdf.iloc[stockindex, 0]
    
    # url time request test
    start_time = time.time()

    tiingoUrl = u1 + stock + u2 + str(start) + u3 + str(end) + token
    
    stock_history = pd.read_json(tiingoUrl)
    stock_history = pd.DataFrame(stock_history)
    type(stock_history)
        
    df = pd.DataFrame({"Open": stock_history["open"],
                       "adjOpen": stock_history["adjOpen"],
                       "High": stock_history["high"],
                       "adjHigh": stock_history["adjHigh"],
                       "Low": stock_history["low"],
                       "adjLow": stock_history["adjLow"],
                       "Close": stock_history["close"],
                       "adjClose": stock_history["adjClose"],
                       "Volume": stock_history["volume"],
                       "adjVolume": stock_history["adjVolume"],
                       "splitFactor": stock_history["splitFactor"],
                       "date": stock_history["date"],
                       })
    df = df.set_index(pd.DatetimeIndex(df["date"]))   
    df = df[['Open', 'adjOpen', 'High', 'adjHigh', 'Low', 'adjLow', 'Close', 'adjClose', 'Volume', 'adjVolume', 'splitFactor']]

    # Create Hierarchical Keys using PyTable format in Pandas (HDF5 file structure):
#    stockGroup = '/history/' + stock
#    
#    stock_history.to_hdf(store, key= stockGroup, format='table', append=True)
    
    end_time = time.time()
    print(end_time - start_time)
    
    stockindex = stockindex + 1
    
#store.close()



