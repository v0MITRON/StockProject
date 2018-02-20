from urllib.request import urlopen, Request
from urllib.error import URLError
import json
from bson import json_util
from pymongo import MongoClient

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

rep = {
        '1. open':'open',
        '2. high':'high',
        '3. low':'low',
        '4. close':'close',
        '5. volume':'volume',
        '1. Information':'information',
        '2. Symbol':'symbol',
        '3. Last Refreshed':'last refreshed',
        '4. Output Size':'output size',
        '5. Time Zone':'time zone'
        }

with open('shortUrlList.txt') as infile:
    for line in infile:
        ticker = line.partition(' ')[0] #line.partition('\t') was being a bitch with an updated shortUrlList.txt file
        baseUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
        sizeKey = '&outputsize=full&apikey=EYYWNSLNIGPKVAJZ'
        url = baseUrl + ticker + sizeKey
        req = Request(url)
        
        numReq = 1
        while numReq < 4:
            try:
                response = urlopen(req)
            except URLError as e:
                if hasattr(e, 'reason'):
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                elif hasattr(e, 'code'):
                    print('The server could not fulfill the request.')
                    print('Error code: ', e.code)
                numReq = numReq + 1
            else:
                numReq = 4
                apiData = response.read().decode('utf-8')

        data = replace_all(apiData, rep)
        #save in a json string
        json_str = json.dumps(data)
        jdata = json.loads(json_str)
        bData = json_util.loads(jdata)

        conn = MongoClient('localhost', 27017)
        db = conn.stockTest
        collection = db.stockHistory
        result = collection.insert_one(bData)
        result.inserted_id



