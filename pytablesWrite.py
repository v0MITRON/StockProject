#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 21:30:51 2018

@author: matt
"""

from urllib.request import urlopen, Request
import pandas as pd
from pandas_datareader import data as web
import datetime
from tables import *
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

# Open/create HDF5 file using pandas
# Compress using default zlib
store = pd.HDFStore('stockData_compressed.h5', complevel=9, complib='zlib')

# Iterate down df pulling stock symbol for history download
stockindex = 0
while stockindex < 5:
    stock = testdf.iloc[stockindex, 0]
    
    stock_history = web.DataReader(stock, "yahoo", start, end)
    type(stock_history)
    
    stock_history = stock_history[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    
    # Create Hierarchical Keys using PyTable format in Pandas (HDF5 file structure):
    stockGroup = '/history/' + stock
    
    stock_history.to_hdf(store, key= stockGroup, format='table', append=True)
    
    #stock_history.close() 
    
    stockindex = stockindex + 1
    
store.close()


