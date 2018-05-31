#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 15:59:17 2018

@author: matt
"""

import requests
import zipfile
import io
import pandas as pd

r = requests.get("https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip")
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

df = pd.read_csv('supported_tickers.csv')

# get only NASDAQ tickers
exchange = df.loc[df['exchange'] == 'NASDAQ']

# get only NASDAQ stock tickers (multiple conditions using df.query)
exchangeStock = df.query('exchange == "NASDAQ" & assetType == "Stock"')

print(exchangeStock.tail(10))