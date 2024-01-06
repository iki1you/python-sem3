import threading
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor


def get_currencies(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        currency = str(soup.find_all('valute')[id])
        if currency not in currencies:
            currencies.append(currency)


if __name__ == '__main__':
    currencies = []
    id = int(input())

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(get_currencies, urls)
        for r in results:
            print(r)

    currencies_string = ''.join(results)
    print(currencies_string)