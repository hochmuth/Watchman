'''Gathers fundamental information about a stock using the Alpha Vantage API.'''
import requests
import pandas as pd

# Local
import secrets

API_URL = 'https://www.alphavantage.co/query'
symbol = 'GOOG'

data = {'function': 'OVERVIEW',
        'symbol': symbol,
        'outputsize': 'full',
        'datatype': 'json',
        'apikey': secrets.alpha_vantage_key}

response = requests.get(API_URL, params=data)
assert response.ok, 'Error in getting response from server'
[print(f'{key}: {response.json()[key]}') for key in response.json()]