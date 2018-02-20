# -*- coding: utf-8 -*-
import pandas as pd
from pandas_datareader import data as web
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np

def pandas_candlestick_ohlc(dat, stick = "day", otherseries = None):
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    dayFormatter = DateFormatter('%d')
    
    transdat = dat.loc[:,["Open", "High", "Low", "Close"]]
    if (type(stick) == str):
        if stick == "day":
            plotdat = transdat
            stick = 1
        elif stick in ["week", "month", "year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1])
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month)
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0])
            grouped = transdat.groupby(list(set(["year",stick])))
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low":[], "Close": []})
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                                       "High": max(group.High),
                                                       "Low": min(group.Low),
                                                       "Close": group.iloc[-1,3]},
                                                        index = [group.index[0]]))
            if stick == "week": stick = 5
            elif stick == "month": stick = 30
            elif stick == "year": stick = 365
    elif (type(stick) == int and stick >= 1):
        transdat["stick"] = [np.floor(i / stick) for i in range(len(transdat.index))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame({"Open": [], "High": [], "Low":[], "Close": []})
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                                       "High": max(group.High),
                                                       "Low": min(group.Low),
                                                       "Close": group.iloc[-1,3]},
                                                        index = [group.index[0]]))
    else:
        raise ValueError('Valid imputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')
    
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)
    
    ax.grid(True)
    
    candlestick_ohlc(ax, list(zip(list(mdates.date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
                                  plotdat["Low"].tolist(), plotdat["Close"].tolist())),
                                    colorup = "black", colordown = "red", width = stick * .4)
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)
    
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    
    plt.show()

start = datetime.datetime(2017, 1, 1)
end = datetime.date.today()

aapl = web.DataReader("AAPL", "yahoo", start, end)

type(aapl)

#simple graph
#aapl["Adj Close"].plot(grid = True)

pandas_candlestick_ohlc(aapl)

