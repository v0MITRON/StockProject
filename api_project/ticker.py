# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import requests
import zipfile
import io
import pandas as pd

libUrl = "https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip"

def lib():
    r = requests.get(libUrl)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()
    
    df = pd.read_csv('supported_tickers.csv')
    
    df = df[['ticker', 'exchange', 'assetType', 'priceCurrency', 'startDate', 'endDate']]
    
    """
    check to see if .h5 file is open.
    if not, open it
    if it is, append the file
    """
    
    store = pd.HDFStore('stockDB.h5', complevel=9, complib='zlib')
    
    df.to_hdf(store, key='/lib/supported_tickers', format='table', append=True)
    
    return
    
    
if __name__ == "__main__":
    print("Hello World")
