#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas_datareader import data as web
from pandas_datareader._utils import RemoteDataError
import datetime
from pandas.tseries.offsets import BDay
import matplotlib.pyplot as plt

ticker = "DDD"
start = datetime.datetime(2007, 1, 1)
end = datetime.date.today()
stock_history = web.DataReader(ticker, "yahoo", start, end)

type(stock_history)

print(stock_history.head(30))

#simple graph
#stock_history["Adj Close"].plot(grid = True)
stock_history["90d"] = np.round(stock_history["Close"].rolling(window = 90, center = False).mean(), 2)
stock_history["200d"] = np.round(stock_history["Close"].rolling(window = 200, center = False).mean(), 2)
stock_history["Close-200d"] = stock_history["Close"] - stock_history["200d"]

stock_history["Regime"] = np.where(stock_history["Close-200d"] > 0, 1, 0) #Bullish
stock_history["Regime"] = np.where(stock_history["Close-200d"] < 0, -1, stock_history["Regime"])

regime_orig = stock_history.ix[-1, "Regime"]
stock_history.ix[-1, "Regime"] = 0
stock_history["Signal"] = np.sign(stock_history["Regime"] - stock_history["Regime"].shift(1))
stock_history.ix[-1, "Regime"] = regime_orig

##Add index column to easily determine min/max dates
##Add other indicator columns +/- and a final column to add scores.  
##  High scores are very bullish, low very bearish
##Then determine % change
##Finally, if a stock is worth looking at

stock_eval = pd.DataFrame({"Open": stock_history["Open"],
                           "High": stock_history["High"],
                           "Low": stock_history["Low"],
                           "Close": stock_history["Close"],
                           "Adj Close": stock_history["Adj Close"],
                           "Volume": stock_history["Volume"],
                           "90d SMA": stock_history["90d"],
                           "200d SMA": stock_history["200d"],
                           "Close - 200d SMA": stock_history["Close-200d"],
                           "Regime": stock_history["Regime"],
                           "Signal": stock_history["Signal"],
                           }).tail(120)
print(stock_eval.tail(120))

stock_min_index = stock_eval.loc[stock_eval["Close"].idxmin()]
stock_min = stock_min_index[2]
stock_max_index = stock_eval.loc[stock_eval["Close"].idxmax()]
stock_max = stock_max_index[2]

print(stock_min_index)








if stock_min_index["Close"] < stock_max_index["Close"]:
    percent_change = ((stock_max_index["Close"] - stock_min_index["Close"])/stock_min_index["Close"] * 100)
else:
    percent_change = ((stock_min_index["Close"] - stock_max_index["Close"])/stock_max_index["Close"] * 100)

print(percent_change)

if stock_eval["Close"].iloc[0] < stock_eval["200d SMA"].iloc[0]:
    i = 1
    try:
        while stock_eval["Close"].iloc[i] < stock_eval["200d SMA"].iloc[i]:
            i = i + 1
        print(ticker + " has moved above the 200 day SMA.")
    except RemoteDataError:
        print(ticker + " failed to move above the 200 day SMA.")
else:
    print(ticker + " stock is already trading above the 200 day SMA.")
    
b = 0
i = 0
while stock_eval["Close"].iloc[i] < 120:
    if stock_eval["Close"].iloc[i] > stock_eval["200d SMA"].iloc[i]:
        if stock_eval["Close"].iloc[i + 1] < stock_eval["200d SMA"].iloc[i + 1]:
            b = b + 1
    i = i + 1

print("Stock has dipped below the 200 day SMA " + str(b) + " times.")
        