# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import requests
import zipfile
import io
import pandas as pd
from urllib.request import urlopen, Request
import datetime

supUrl = "https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip"
u1 = "https://api.tiingo.com/tiingo/daily/"
u2 = "/prices?startDate="
u3 = "&endDate="
token = "&token=e03a22d17056b77d1938b28fabfeea3f668a617a"
n1 = "https://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange="
n2 = "&render=download"


def lib():
    store = pd.HDFStore('stockDB.h5', complevel=9, complib='zlib')

    rundate = datetime.date.today()
    filterdate = rundate - datetime.timedelta(days=5)

    r = requests.get(supUrl)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()

    df = pd.read_csv('supported_tickers.csv')
    df = df[['ticker', 'exchange', 'assetType', 'priceCurrency',
            'startDate', 'endDate']]

    def appendInfo(exchange):
        url = n1 + exchange + n2
        csv = exchange + ".csv"

        with urlopen(Request(url)) as testfile, open(csv, 'w') as f:
            f.write(testfile.read().decode())

        appendf = pd.read_csv(csv, usecols=['Symbol', 'Name', 'MarketCap',
                                          'IPOyear', 'Sector', 'industry'])

        return appendf

    tempdf = appendInfo('nyse')
    tempdf.append(appendInfo('nasdaq'), ignore_index=True)
    tempdf.append(appendInfo('amex'), ignore_index=True)
    
    appdf = pd.DataFrame({'ticker': tempdf['Symbol'],
                               'name': tempdf['Name'],
                               'marketCap': tempdf['MarketCap'],
                               'IPOyear': tempdf['IPOyear'],
                               'sector': tempdf['Sector'],
                               'industry': tempdf['industry']})

    df = df.merge(appdf, on='ticker', how='left')
    exchange_list = ['NYSE', 'NASDAQ', 'AMEX']
    df['endDate'] = pd.to_datetime(df['endDate'])
    df = df[(df['endDate'] > filterdate) & df.exchange.isin(exchange_list)]
    df = df.query('assetType == "Stock"')

    df.to_hdf(store, key='/lib/supported_tickers', format='table', append=True)

    store.close()

    return


def irequest(symbol, startDate, endDate):
    tiingoUrl = u1 + symbol + u2 + str(startDate) + u3 + str(endDate) + token

    stock_history = pd.read_json(tiingoUrl)
    stock_history = pd.DataFrame(stock_history)
    type(stock_history)


if __name__ == "__main__":
    print("Hello World")
