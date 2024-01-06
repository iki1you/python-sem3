import json
import bs4

# html = input()
with open('1.txt', encoding='utf-8') as file:
    soup = bs4.BeautifulSoup(file, 'html.parser')

exchange = {
    '₽': 1.0,
    '$': 100.0,
    '€': 105.0,
    '₸': 0.210,
    'Br': 30.0,
}

result = {
    'vacancy': None,
    'salary': None,
    'experience': None,
    'company': None,
    'description': None,
    'skills': None,
    'created_at': None,
}

for i in soup.findAll('p', class_='vacancy-title'):
    print(i.text)