'''Gathers fundamental information about a stock using the Alpha Vantage API.'''
import os
import requests
import datetime
import time
import pandas as pd
import secrets

from ratelimit import limits, sleep_and_retry
from functions import *
from metrics import metric_map

API_URL = 'https://www.alphavantage.co/query'
api_key = secrets.ALPHAVANTAGE_API_KEY
api_tickers = ['MKL', 'AAPL', 'AMZN']

api_functions = ['OVERVIEW',
                 'INCOME_STATEMENT',
                 'BALANCE_SHEET',
                 'CASH_FLOW']

if __name__ == '__main__':

    # API rate limit
    if len(api_tickers) > 1:
        time.sleep(60)
    start_time = time.time()

    # Query the API
    api_results = get_fundamentals_from_api(tickers=api_tickers,
                                            functions=api_functions,
                                            api_url=API_URL,
                                            api_key=api_key)
    for ticker in api_tickers:
        # Save the annual results into csv
        df_annual = annual_data_into_df(ticker, metric_map, api_results, trim_key=True)
        df_to_csv(df=df_annual,
                  folder='./annual_reports',
                  ticker=ticker,
                  report_type='annual',
                  year=df_annual.index.max())

        # Save overview into csv
        df_overview = overview_into_df(ticker, api_results)
        df_to_csv(df=overview_into_df(ticker, api_results),
                  folder='./overviews',
                  ticker=ticker,
                  report_type='overview',
                  year=df_overview.loc['LatestQuarter'].values[0][:4])

    # How long it took
    running_time = time.time() - start_time
    if running_time < 60:
        print(f'Total running time: {round(running_time)} sec')
    else:
        print(f'Total running time: {round(running_time/60)} min')