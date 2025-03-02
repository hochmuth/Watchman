import os
import requests
import pandas as pd
import secrets

API_URL = 'https://www.alphavantage.co/query'
symbol = 'GOOG'

data = {'function': 'OVERVIEW',
        'symbol': symbol,
        'outputsize': 'full',
        'datatype': 'json',
        'apikey': os.getenv('ALPHAVANTAGE_API_KEY')}

response = requests.get(API_URL, params=data)
assert response.ok, 'Error in getting response from server'
print('Ok')

