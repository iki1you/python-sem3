import csv
import math
import re

import prettytable
from prettytable import PrettyTable



def drop_extra_spaces(line):
    return ' '.join(filter(lambda x: not x.isspace(), ', '.join([i.strip() for i in line.split('\n')]).split()))


def drop_tags(line):
    return re.sub(r'<.*?>', '', line)


def csv_reader(file_name):
    with open(file_name, encoding='utf-8-sig') as file:
        data = [i for i in csv.reader(file)]
    if len(data) == 0:
        return 'Пустой файл'
    return (data[0],
            list(filter(lambda x: len(x) == len(data[0]), filter(lambda x: all([len(e) > 0 for e in x]), data[1:]))))


def csv_filer(reader, list_naming):
    vacancies = []
    for i in list_naming:
        vacancy = dict()
        for j, key in enumerate(reader):
            vacancy[key] = drop_extra_spaces(drop_tags(i[j])).strip()
        vacancies.append(vacancy)
    return vacancies


def change_data_format(s):
    for j in re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}', s):
        s = s.replace(j, (j[8:10] + '.' + j[5:7] + '.' + j[0:4]).replace(':', '-'))
    return s


def format_salary(k):
    k = str(math.floor(float(k)))
    total = []
    while len(k) >= 3:
        total.append(k[-3:])
        k = k[:-3]
    total = list(reversed(total))
    total.insert(0, k)
    return ' '.join(total).strip()


def skills_format(line):
    return '\n'.join(line.split(', '))


def slice_line(line):
    if len(line) > 100:
        return line[:100] + '...'
    return line


def formatter(row):
    gross = '(Без вычета налогов)'
    if row['salary_gross'] == 'False':
        gross = '(С вычетом налогов)'
    format_bool = {'false': 'Нет', 'true': 'Да'}
    format_row = {
        'name': row['name'],
        'description': row['description'],
        'key_skills': skills_format(row['key_skills']),
        'experience_id': work_exp[row['experience_id']],
        'premium': format_bool[row['premium'].lower()],
        'employer_name': row['employer_name'],
        'salary': f'{format_salary(row["salary_from"])} - {format_salary(row["salary_to"])} '
                  f'({currency[row["salary_currency"]]}) {gross}',
        'area_name': row['area_name'],
        'published_at': change_data_format(row['published_at'])
    }

    return format_row


def get_table(data_vacancies):
    if len(data_vacancies) == 0:
        return 'Нет данных'
    mytable = PrettyTable()
    mytable.hrules = prettytable.ALL
    mytable.align = 'l'
    mytable.field_names = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия',
                           'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии']
    mytable.max_width = 20
    for i in range(len(data_vacancies)):
        mytable.add_row(list(map(lambda x: slice_line(x), formatter(data_vacancies[i]).values())))
    mytable.add_autoindex('№')
    return mytable


work_exp = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"
}

currency = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум"
}

naming = {
    'name': 'Название',
    'description': 'Описание',
    'key_skills': 'Навыки',
    'experience_id': 'Опыт работы',
    'premium': 'Премиум-вакансия',
    'employer_name': 'Компания',
    'salary_from': 'Нижняя граница вилки оклада',
    'salary_to': 'Верхняя граница вилки оклада',
    'salary_gross': 'Без вычета налогов',
    'salary_currency': 'Идентификатор валюты оклада',
    'area_name': 'Название региона',
    'published_at': 'Дата публикации вакансии',
    'salary': 'Оклад'
}


reader = csv_reader(input())

if reader == 'Пустой файл':
    print('Пустой файл')
else:
    print(get_table(csv_filer(*reader)))


# создание экземпляра
