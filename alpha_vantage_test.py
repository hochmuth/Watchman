import requests
import pandas as pd
import secrets

API_URL = 'https://www.alphavantage.co/query'
symbol = 'GOOG'

data = {'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'full',
        'datatype': 'json',
        'apikey': secrets.alpha_vantage_key}

response = requests.get(API_URL, data)

print(response.json())
