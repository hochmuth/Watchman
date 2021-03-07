import requests
import pandas as pd
import secrets

API_URL = 'https://www.alphavantage.co/query'
symbol = 'GOOG'

data = {'function': 'INCOME_STATEMENT',
        'symbol': symbol,
        'outputsize': 'full',
        'datatype': 'json',
        'apikey': secrets.alpha_vantage_key}

response = requests.get(API_URL, params=data)
assert response.ok, 'Error in getting response from server'
print('Ok')

