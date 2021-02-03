import requests
from bs4 import BeautifulSoup

base_url = 'https://finance.yahoo.com/quote/QUOTE/key-statistics?p=QUOTE'
quotes = ['INTC', 'BIIB', 'MKL']


for quote in quotes:

    page = requests.get(base_url.replace('QUOTE', quote))
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get price
    header = soup.find(id="quote-header-info")
    elems_price = header.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
    # print(type(elems_price))
    [print(f'{quote}: {elem.text.strip()}') for elem in elems_price]

    val_table = soup.find(id='mrt-node-Col1-0-KeyStatistics')
    elems_pe_ratio = val_table.find_all('tr', class_='Bxz(bb) H(36px) BdB Bdbc($seperatorColor) fi-row Bgc($hoverBgColor):h')
    # [print(elem) for elem in elems_pe_ratio]
    print(val_table.find('td', attrs={'data-reactid':'28'}).text.strip())
