import csv
import math
import re
import prettytable


def drop_extra_spaces(line):
    s = ''
    for i in line:
        if not (i.isspace() and i != ' ' and i != '\n'):
            s += i
        else:
            s += ' '
    line = s
    while '  ' in line:
        line = line.replace('  ', ' ')
    line = line.strip()
    return line


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
            vacancy[key] = drop_extra_spaces(drop_tags(i[j]))
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

    return line


def slice_line(line):
    if len(line) > 100:
        return line[:100] + '...'
    return line


def formatter(row):
    if row['salary_gross'].capitalize() == 'False':
        gross = '(С вычетом налогов)'
    else:
        gross = '(Без вычета налогов)'
    format_row = {
        'name': row['name'],
        'description': row['description'],
        'key_skills': skills_format(row['key_skills']),
        'experience_id': work_exp[row['experience_id']],
        'premium': {'false': 'Нет', 'true': 'Да'}[row['premium'].lower()],
        'employer_name': row['employer_name'],
        'salary': f'{format_salary(row["salary_from"])} - {format_salary(row["salary_to"])} '
                  f'({currency[row["salary_currency"]]}) {gross}',
        'area_name': row['area_name'],
        'published_at': change_data_format(row['published_at'])
    }
    return format_row


def get_table(data_vacancies, filter_arg):
    if len(data_vacancies) == 0:
        return 'Нет данных'

    mytable = prettytable.PrettyTable()
    mytable.hrules = prettytable.ALL
    mytable.align = 'l'
    mytable.field_names = ['№', 'Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия',
                           'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии']
    mytable.max_width = 20
    k = 1
    for i in range(len(data_vacancies)):
        if filter_row(data_vacancies[i], filter_arg):
            data_row = list(formatter(data_vacancies[i]).values())
            data_row.insert(0, str(k))
            row = list(map(lambda x: slice_line(x), data_row))
            mytable.add_row(row)
            k += 1
    return mytable


def get_format_table(filename, start, end, fields, filter_arg):
    reader = csv_reader(filename)
    if reader == 'Пустой файл':
        return 'Пустой файл'
    table = get_table(csv_filer(*reader), filter_arg)
    if table == 'Нет данных':
        return 'Нет данных'
    if end is None:
        end = len(table.rows)
    if len(table.rows) == 0:
        return 'Ничего не найдено'
    if len(fields) == 0:
        return table.get_string(start=start, end=end)
    fields.append('№')
    return table.get_string(start=start, end=end, fields=fields)


def get_total_table():
    filename = input()
    filter_arg = input()
    limit = input().split()

    if len(limit) == 0:
        start, end = 0, None
    else:
        if len(limit) == 1:
            start, end = int(limit[0]) - 1, None
        else:
            start, end = map(lambda x: int(x) - 1, limit)
    fields = input()

    if fields != '':
        fields = list(fields.split(', '))
    if filter_arg != '':
        if ': ' not in filter_arg:
            return 'Формат ввода некорректен'
        if filter_arg.split(':')[0] not in filter_fields.keys():
            return 'Параметр поиска некорректен'
    table = get_format_table(filename, start, end, fields, filter_arg)
    return table

def skills_compare(row, value):
    skills = set(value[1].split(', '))
    row_skills = set(row['key_skills'].split('\n'))
    return skills.issubset(row_skills)


def currency_compare(row, value):
    return currency[row['salary_currency']] == value[1]


def filter_row(row, filter_arg):
    if filter_arg == '':
        return True
    filter_arg = filter_arg.split(': ')
    if filter_fields[filter_arg[0]](row, filter_arg):
        return True
    return False


def date_compare(row, value):
    date_row = change_data_format(row['published_at'])
    date_value = re.findall(r'\d{2}.\d{2}.\d{4}', value[1])[0]
    return date_row == date_value



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

filter_fields = {
    'Название': lambda row, value: row['name'] == value[1],
    'Описание': lambda row, value: row['description'] == value[1],
    'Компания': lambda row, value: row['employer_name'] == value[1],
    'Навыки': skills_compare,
    'Опыт работы': lambda row, value: work_exp[row['experience_id']] == value[1],
    'Премиум-вакансия': lambda row, value: {'False': 'Нет', 'True': 'Да'}[row['premium']].lower() == value[1].lower(),
    'Оклад': lambda row, value: int(row["salary_from"]) <= int(value[1]) <= int(row["salary_to"]),
    'Название региона': lambda row, value: row['area_name'] == value[1],
    'Дата публикации вакансии': date_compare,
    'Идентификатор валюты оклада': currency_compare
}

a = get_total_table()
print(a)


# vacancies.csv
# Идентификатор валюты оклада: Рубли
# 1
# Название, Навыки, Компания, Оклад, Название региона