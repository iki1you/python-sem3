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
    if len(vacancies) == 0:
        return 'Нет данных'
    return vacancies


def log_function(input_func):
    def output_func(*args):
        filename, filter_arg, sort_key, reverse_arg = args
        vacancies = input_func(*args)
        if vacancies == 'Пустой файл':
            return 'Пустой файл'
        if vacancies == 'Нет данных':
            return 'Нет данных'
        vacancies = sort_table(vacancies, sort_key, reverse_arg)
        k = 1
        total_vacancies = []
        for i in range(len(vacancies)):
            if filter_row(vacancies[i], filter_arg):
                data_row = list(formatter(vacancies[i]).values())
                data_row.insert(0, str(k))
                row = list(map(lambda x: slice_line(x), data_row))
                total_vacancies.append(row)
                k += 1
        if len(total_vacancies) == 'Ничего не найдено':
            return 'Ничего не найдено'
        return total_vacancies

    return output_func


@log_function
def csv_parser(file_name, filter_arg, sort_key, reverse_arg):
    reader = csv_reader(file_name)
    if reader == 'Пустой файл':
        return 'Пустой файл'
    vacancies = csv_filer(*reader)
    if vacancies == 'Нет данных':
        return 'Нет данных'
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
        'key_skills': row['key_skills'],
        'experience_id': work_exp[row['experience_id']],
        'premium': {'false': 'Нет', 'true': 'Да'}[row['premium'].lower()],
        'employer_name': row['employer_name'],
        'salary': f'{format_salary(row["salary_from"])} - {format_salary(row["salary_to"])} '
                  f'({currency[row["salary_currency"]]}) {gross}',
        'area_name': row['area_name'],
        'published_at': change_data_format(row['published_at'])
    }
    return format_row


def get_table(data_vacancies, filter_arg, sort_key, reverse_arg):
    mytable = prettytable.PrettyTable()
    mytable.hrules = prettytable.ALL
    mytable.align = 'l'
    mytable.field_names = ['№', 'Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия',
                           'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии']
    mytable.max_width = 20
    for i in data_vacancies:
        mytable.add_row(i)

    return mytable


def get_format_table(filename, start, end, fields, filter_arg, sort_key, reverse_arg):
    data_vacancies = csv_parser(filename, filter_arg, sort_key, reverse_arg)
    if data_vacancies == 'Пустой файл':
        return 'Пустой файл'
    if data_vacancies == 'Нет данных':
        return 'Нет данных'
    table = get_table(data_vacancies, filter_arg, sort_key, reverse_arg)

    if end is None:
        end = len(table.rows)
    if len(table.rows) == 0:
        return 'Ничего не найдено'
    if len(fields) == 0:
        return table.get_string(start=start, end=end)
    fields.append('№')

    return table.get_string(start=start, end=end, fields=fields)


def get_total_table():
    filename = input('Введите название файла: ')
    filter_arg = input('Введите параметр фильтрации: ')
    sort_arg = input('Введите параметр сортировки: ')
    reverse_arg = input('Обратный порядок сортировки (Да / Нет): ')
    limit = input('Введите диапазон вывода: ').split()
    fields = input('Введите требуемые столбцы: ')

    if filter_arg != '':
        if ': ' not in filter_arg:
            return 'Формат ввода некорректен'
        if filter_arg.split(':')[0] not in filter_fields.keys():
            return 'Параметр поиска некорректен'

    if sort_arg != '' and sort_arg not in sort_keys.keys():
        return 'Параметр сортировки некорректен'
    if reverse_arg != '' and reverse_arg not in ['Да', 'Нет']:
        return 'Порядок сортировки задан некорректно'

    if len(limit) == 0:
        start, end = 0, None
    else:
        if len(limit) == 1:
            start, end = int(limit[0]) - 1, None
        else:
            start, end = map(lambda x: int(x) - 1, limit)

    if fields != '':
        fields = list(fields.split(', '))

    return get_format_table(filename, start, end, fields, filter_arg, sort_arg, reverse_arg)


def sort_table(table, sort_key, reverse_arg):
    if sort_key == '':
        return table
    if reverse_arg == '':
        reverse_arg = 'Нет'
    table.sort(key=sort_keys[sort_key], reverse={'Нет': False, 'Да': True}[reverse_arg])
    return table


def skills_compare(row, value):
    skills = set(value[1].split(', '))
    row_skills = set(row['key_skills'].split('\n'))
    return skills.issubset(row_skills)


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
    'Премиум-вакансия': lambda row, value: {'false': 'нет', 'true': 'да'}[row['premium'].lower()] == value[1].lower(),
    'Оклад': lambda row, value: int(row["salary_from"]) <= int(value[1]) <= int(row["salary_to"]),
    'Название региона': lambda row, value: row['area_name'] == value[1],
    'Дата публикации вакансии': date_compare,
    'Идентификатор валюты оклада': lambda row, value: currency[row['salary_currency']] == value[1]
}

work_exp_sort = {
    "noExperience": 1,
    "between1And3": 2,
    "between3And6": 3,
    "moreThan6": 4
}

sort_keys = {
    'Оклад': lambda x: (int(x['salary_from']) + int(x['salary_to'])) * currency_to_rub[x['salary_currency']] / 2,
    'Название': lambda x: x['name'],
    'Описание': lambda x: x['description'],
    'Компания': lambda x: x['employer_name'],
    'Навыки': lambda x: len(re.split(r'\n', x['key_skills'])),
    'Опыт работы': lambda x: work_exp_sort[x['experience_id']],
    'Премиум-вакансия': lambda x: x['premium'],
    'Название региона': lambda x: x['area_name'],
    'Дата публикации вакансии': lambda x: x['published_at'],
    'Идентификатор валюты оклада': lambda x: x['salary_currency'],
}

currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}

a = get_total_table()
print(a)

# vacancies.csv
# Оклад: 100000
# Оклад
# Нет
# 10 20
# Название, Навыки, Опыт работы, Компания
