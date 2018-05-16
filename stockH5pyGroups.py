#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 20:02:30 2018

@author: matt
"""
from urllib.request import urlopen, Request
import pandas as pd
from pandas_datareader import data as web
import datetime
import h5py
import numpy as np

start = datetime.datetime(2008, 1, 1)
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

f = h5py.File('stockHistory.hdf5', 'w')

# Iterate down df pulling stock symbol for history download
stockindex = 0
while stockindex < 5:
    stock = testdf.iloc[stockindex, 0]
    
    stock_history = web.DataReader(stock, "yahoo", start, end)
    type(stock_history)
    
    stock_history = stock_history[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    
    GROUPNAME = stock
    grouph5 = stock + '.h5'
    
    dset = stock_history.to_hdf(grouph5, 'table', append=True)
    
    f.create_group(dset)
    
    
        
    stockindex = stockindex + 1
    
f.close()


