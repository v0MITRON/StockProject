#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import datetime
from pandas_datareader import data as web

def ohlc_adj(dat):
    """
    :param dat: pandas DataFrame with stock data, including "Open", "High", "Low", "Close", and "Adj Close", with "Adj Close" containing adjusted closing prices
 
    :return: pandas DataFrame with adjusted stock data
 
    This function adjusts stock data for splits, dividends, etc., returning a data frame with
    "Open", "High", "Low" and "Close" columns. The input DataFrame is similar to that returned
    by pandas Yahoo! Finance API.
    """
    return pd.DataFrame({"Open": dat["Open"] * dat["Adj Close"] / dat["Close"],
                       "High": dat["High"] * dat["Adj Close"] / dat["Close"],
                       "Low": dat["Low"] * dat["Adj Close"] / dat["Close"],
                       "Close": dat["Adj Close"]})

start = datetime.datetime(2016, 1, 1)
end = datetime.date.today()

aapl = web.DataReader("AAPL", "yahoo", start, end)

type(aapl)
    
aapl_adj = ohlc_adj(aapl)