import requests
from bs4 import BeautifulSoup

url = 'https://finance.yahoo.com/quote/BIIB/key-statistics?p=BIIB'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id="quote-header-info")
# print(results.prettify())
job_elems = results.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
[print(elem.text.strip()) for elem in job_elems]