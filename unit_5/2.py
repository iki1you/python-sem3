import csv
import math
import re


def drop_extra_spaces(line):
    return ' '.join(filter(lambda x: not x.isspace(), ', '.join([i.strip() for i in line.split('\n')]).split()))


def drop_tags(line):
    return re.sub(r'<.*?>', '', line)


def csv_reader(file_name):
    with open(file_name, encoding='utf-8-sig') as file:
        data = [i for i in csv.reader(file)]
    return (data[0],
            list(filter(lambda x: len(x) == len(data[0]), filter(lambda x: all([len(e) > 0 for e in x]), data[1:]))))


# drop_tags + drop_extra_spaces
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


def formatter(row):
    gross = '(Без вычета налогов)'
    if row['salary_gross'] == 'False':
        gross = '(С вычетом налогов)'
    format_bool = {'false': 'Нет', 'true': 'Да'}
    format_row = {
        'name': row['name'],
        'description': row['description'],
        'key_skills': row['key_skills'],
        'experience_id': work_exp[row['experience_id']],
        'premium': format_bool[row['premium'].lower()],
        'employer_name': row['employer_name'],
        'salary': f'{format_salary(row["salary_from"])} - {format_salary(row["salary_to"])} '
                  f'({currency[row["salary_currency"]]}) {gross}',
        'area_name': row['area_name'],
        'published_at': change_data_format(row['published_at'])
    }

    return format_row


def print_vacancies(data_vacancies, dic_naming):
    for i in range(len(data_vacancies)):
        for key, value in formatter(data_vacancies[i]).items():
            print(f'{dic_naming[key]}: {value}')
        if len(data_vacancies) - i - 1 != 0:
            print()


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


print_vacancies(csv_filer(*csv_reader(input())), naming)