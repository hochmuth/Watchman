# Functions used in the Watchman project
import os
import requests
import datetime
import time
import pandas as pd
import secrets

from ratelimit import limits, sleep_and_retry


def annual_data_into_df(ticker, metric_map, json_data, trim_key=False):
    df_annual = pd.DataFrame()
    for statement in metric_map:
        for metric in metric_map[statement]:
            df_tmp = get_annual_data(data=json_data,
                                     ticker=ticker,
                                     fin_statement=statement,
                                     fin_metric=metric).sort_index().astype('float')
            if df_annual.empty:
                df_annual = df_tmp
            else:
                df_annual = df_annual.join(df_tmp, how='inner')
    df_annual.sort_index(inplace=True)
    if trim_key:
        df_annual.index = df_annual.index.str[:4]
    return df_annual


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


def df_to_csv(df, folder, ticker, report_type, year):
    out_name = f'{folder}/{ticker}_{year}_{report_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(out_name, sep=';', encoding='utf8')


def get_annual_data(data, ticker, fin_statement, fin_metric):
    return pd.DataFrame.from_records([(record['fiscalDateEnding'], record[fin_metric])
                                      for record in data[ticker][fin_statement]['annualReports']],
                                     columns=['fiscalYear', fin_metric]).set_index('fiscalYear').replace('None', 0)


def get_fundamentals_from_api(tickers, functions, api_url, api_key):
    out_dict = dict()
    for ticker in tickers:
        print(f'Gathering {ticker}')
        fund_dict = dict()
        for i, function in enumerate(functions):
            # API limit
            if i > 0 and i % 4 == 0:
                time.sleep(60)
            response = call_api(api_url, api_data_function(ticker, function, api_key))
            assert response.ok, f'Error in getting response from server. Ticker {ticker}, function {function}'
            fund_dict[function] = response.json()
        out_dict[ticker] = fund_dict
        # API limit
        time.sleep(60)
    return out_dict


def overview_into_df(ticker, json_data):
    df = pd.Series(dict(json_data[ticker]['OVERVIEW'])).to_frame().rename(columns={0: 'Value'})
    df.index.rename('Metric', inplace=True)
    return df
