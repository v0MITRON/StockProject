import ticker
import pandas as pd

ticker.lib()

file = '/home/matt/Projects/Stock Project/API_project/api_project/stockDB.h5'

table = pd.read_hdf(file, '/lib/supported_tickers')

print(table.tail(100))
