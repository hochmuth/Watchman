'''Gathers fundamental information about a stock using the Alpha Vantage API.'''
import os
import requests
import time
import pandas as pd

from ratelimit import limits, sleep_and_retry


API_URL = 'https://www.alphavantage.co/query'
api_key = os.getenv('ALPHAVANTAGE_API_KEY')
api_tickers = ['GOOG']

api_functions = ['OVERVIEW',
                 'INCOME_STATEMENT',
                 'BALANCE_SHEET',
                 'CASH_FLOW']


def api_data_function(symbol, function, apikey):
    return {'function': function,
        'symbol': symbol,
        'outputsize': 'full',
        'datatype': 'json',
        'apikey': apikey}


@sleep_and_retry
@limits(calls=5, period=60)
def call_api(url, data):
    return requests.get(url, params=data)


def get_fundamentals_from_api(tickers, functions):
    out_dict = dict()
    for ticker in tickers:
        fund_dict = dict()
        for function in functions:
            response = call_api(API_URL, api_data_function(ticker, function, api_key))
            assert response.ok, f'Error in getting response from server. Ticker {ticker}, function {function}'
            fund_dict[function] = response.json()
        out_dict[ticker] = fund_dict
    return out_dict


if __name__ == '__main__':
    time.sleep(60)
    start_time = time.time()

    api_results = get_fundamentals_from_api(api_tickers, api_functions)
    for result in api_results:
        print(result)
        [print(api_results[result][func]) for func in api_results[result]]

    print(f'Total running time: {time.time() - start_time}')