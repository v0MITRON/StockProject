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

# Iterate down df pulling stock symbol for history download
stockindex = 0
while stockindex < 5:
    stock = testdf.iloc[stockindex, 0]
    
    stock_history = web.DataReader(stock, "yahoo", start, end)
    type(stock_history)
    
    stock_history = stock_history[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    
    GROUPNAME = stock
    grouph5 = stock + '.h5'
    
    stock_history.to_hdf(grouph5, 'table', append=True)
    
    #stock_history.close() 
    
    stockindex = stockindex + 1
    



