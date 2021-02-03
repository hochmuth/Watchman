import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

base_url = 'https://finance.yahoo.com/quote/QUOTE/key-statistics?p=QUOTE'
quotes = ['INTC', 'BIIB', 'MKL']
val_fetched = []
val_fetched_rows = []

verbose = True

for quote in quotes:
    if verbose: print(f'Parsing {quote}')

    page = requests.get(base_url.replace('QUOTE', quote))
    soup = BeautifulSoup(page.content, 'html.parser')
    timestamp = datetime.datetime.now()

    # Get price
    header = soup.find(id="quote-header-info")
    elems_price = header.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')

    # Get statistics
    val_id_map = {'Market Cap': '21',
                  'Enterprise Value': '28',
                  'Trailing P/E': '35',
                  'Forward P/E': '42',
                  'Price/Sales': '56',
                  'Price/Book': '63',
                  'Profit Margin': '344',
                  'Operating Margin': '351',
                  'Return on Assets': '365',
                  'Return on Equity': '372',
                  'Revenue': '386',
                  'Revenue Per Share': '393',
                  'Gross Profit': '407',
                  'Net Income': '421',
                  'Diluted EPS': '428',
                  'Total Cash': '449',
                  'Total Debt': '463',
                  'Current Ratio': '477',
                  'Book Value Per Share': '484',
                  'Operating Cash Flow': '498',
                  'Levered Free Cash Flow': '505'}

    val_table = soup.find(id='mrt-node-Col1-0-KeyStatistics')
    val_dict_tmp = dict()
    val_dict_tmp['Quote'] = quote
    val_dict_tmp['Timestamp'] = timestamp

    for val in val_id_map:
        fetched_tmp = val_table.find('td', attrs={'data-reactid': val_id_map[val]})
        fetched_text_tmp = fetched_tmp.text.strip() if fetched_tmp is not None else 'N/A'
        val_fetched.append((quote, val, fetched_text_tmp))
        val_dict_tmp[val] = fetched_text_tmp

    val_fetched_rows.append(val_dict_tmp)

# Store the output in a csv file
df_out = pd.DataFrame(val_fetched_rows)
df_out.to_csv('./fin_stats.csv',
              header=True,
              sep=';',
              mode='a',
              index=False)
