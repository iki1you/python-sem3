import csv
import math
import re

import prettytable


class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = self.write_vacancies()

    def write_vacancies(self):
        vacancies = self.csv_parser(self.file_name)
        if vacancies == 'Пустой файл':
            return 'Пустой файл'
        total = []
        for i in vacancies:
            vacancy = Vacancy()
            vacancy.name = i['name']
            vacancy.salary = Salary(i['salary_from'], i['salary_to'], i['salary_gross'], i['salary_currency'])
            vacancy.premium = i['premium']
            vacancy.employer_name = i['employer_name']
            vacancy.area_name = i['area_name']
            vacancy.description = i['description']
            vacancy.experience_id = i['experience_id']
            vacancy.key_skills = i['key_skills'].split('\n')
            vacancy.published_at = i['published_at']
            total.append(vacancy)
        return total

    @staticmethod
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

    @staticmethod
    def drop_tags(line):
        return re.sub(r'<.*?>', '', line)

    @staticmethod
    def csv_parser(file_name):
        def csv_reader(csv_name):
            with open(csv_name, encoding='utf-8-sig') as file:
                data = [i for i in csv.reader(file)]
            if len(data) == 0:
                return 'Пустой файл'
            return (data[0],
                    list(
                        filter(lambda x: len(x) == len(data[0]),
                               filter(lambda x: all([len(e) > 0 for e in x]), data[1:]))))

        def csv_filer(r, list_naming):
            csv_vacancies = []
            for i in list_naming:
                vacancy = dict()
                for j, key in enumerate(r):
                    vacancy[key] = DataSet.drop_extra_spaces(DataSet.drop_tags(i[j]))
                csv_vacancies.append(vacancy)
            return csv_vacancies

        reader = csv_reader(file_name)
        if reader == 'Пустой файл':
            return 'Пустой файл'
        vacancies = csv_filer(*reader)
        return vacancies


class Vacancy:
    work_exp = {
        "noExperience": "Нет опыта",
        "between1And3": "От 1 года до 3 лет",
        "between3And6": "От 3 до 6 лет",
        "moreThan6": "Более 6 лет"
    }

    def __init__(self):
        self.name = ''
        self.description = ''
        self.key_skills = []
        self.experience_id = ''
        self.premium = ''
        self.employer_name = ''
        self.salary = object
        self.area_name = ''
        self.published_at = ''

    def get_row(self):
        return [self.slice_line(self.name), self.slice_line(self.description),
                self.slice_line('\n'.join(self.key_skills)), self.slice_line(Vacancy.work_exp[self.experience_id]),
                self.slice_line({'false': 'Нет', 'true': 'Да'}[self.premium.lower()]),
                self.slice_line(self.employer_name),
                self.slice_line(str(self.salary)), self.slice_line(self.area_name),
                self.slice_line(self.change_data_format(self.published_at))]

    @staticmethod
    def slice_line(line):
        if len(line) > 100:
            return line[:100] + '...'
        return line

    @staticmethod
    def change_data_format(s):
        for j in re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}', s):
            s = s.replace(j, (j[8:10] + '.' + j[5:7] + '.' + j[0:4]).replace(':', '-'))
        return s


class Salary:
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

    def __init__(self, *args):
        self.salary_from, self.salary_to, self.salary_gross, self.salary_currency = args

    @staticmethod
    def format_salary(k):
        k = str(math.floor(float(k)))
        total = []
        while len(k) >= 3:
            total.append(k[-3:])
            k = k[:-3]
        total = list(reversed(total))
        total.insert(0, k)
        return ' '.join(total).strip()

    def __str__(self):
        if self.salary_gross.capitalize() == 'False':
            gross = '(С вычетом налогов)'
        else:
            gross = '(Без вычета налогов)'
        return (f'{self.format_salary(self.salary_from)} - {self.format_salary(self.salary_to)} '
                f'({self.currency[self.salary_currency]}) {gross}')


class InputConnect:
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

    filter_fields = {
        'Название': lambda vacancy, value: vacancy.name == value,
        'Описание': lambda vacancy, value: vacancy.description == value,
        'Компания': lambda vacancy, value: vacancy.employer_name == value,
        'Навыки': lambda vacancy, value: set(value.split(', ')).issubset(set(vacancy.key_skills)),
        'Опыт работы': lambda vacancy, value: Vacancy.work_exp[vacancy.experience_id] == value,
        'Премиум-вакансия': lambda vacancy, value: {'false': 'нет', 'true': 'да'}[
                                                       vacancy.premium.lower()] == value.lower(),
        'Оклад': lambda vacancy, value: int(vacancy.salary.salary_from) <= int(value) <= int(vacancy.salary.salary_to),
        'Название региона': lambda vacancy, value: vacancy.area_name == value,
        'Дата публикации вакансии': lambda vacancy, value: Vacancy.change_data_format(
            vacancy.published_at) == re.findall(r'\d{2}.\d{2}.\d{4}', value)[0],
        'Идентификатор валюты оклада': lambda vacancy, value: InputConnect.currency[vacancy.salary.salary_currency] == value
    }

    work_exp_sort = {
        "noExperience": 1,
        "between1And3": 2,
        "between3And6": 3,
        "moreThan6": 4
    }

    sort_keys = {
        'Оклад': lambda x: (int(x.salary.salary_from) + int(x.salary.salary_to)) * Salary.currency_to_rub[
            x.salary.salary_currency] / 2,
        'Название': lambda x: x.name,
        'Описание': lambda x: x.description,
        'Компания': lambda x: x.employer_name,
        'Навыки': lambda x: len(x.key_skills),
        'Опыт работы': lambda x: InputConnect.work_exp_sort[x.experience_id],
        'Премиум-вакансия': lambda x: x.premium,
        'Название региона': lambda x: x.area_name,
        'Дата публикации вакансии': lambda x: x.published_at,
        'Идентификатор валюты оклада': lambda x: x.salary_currency,
    }

    def __init__(self, *args):
        self.filename, self.filter_arg, self.sort_arg, self.reverse_arg, self.limit, self.fields = args
        self.start = 0
        self.end = 0

    def input_correct(self):
        if self.filter_arg != '':
            if ': ' not in self.filter_arg:
                return 'Формат ввода некорректен'
            if self.filter_arg.split(':')[0] not in self.filter_fields.keys():
                return 'Параметр поиска некорректен'

        if self.sort_arg != '' and self.sort_arg not in self.sort_keys.keys():
            return 'Параметр сортировки некорректен'
        if self.reverse_arg != '' and self.reverse_arg not in ['Да', 'Нет']:
            return 'Порядок сортировки задан некорректно'

        if len(limit) == 0:
            self.start, self.end = 0, None
        else:
            if len(limit) == 1:
                self.start, self.end = int(self.limit[0]) - 1, None
            else:
                self.start, self.end = map(lambda x: int(x) - 1, self.limit)

        if self.fields != '':
            self.fields = list(self.fields.split(', '))

        return 0

    def work_vacancies(self, data_vacancies):

        vacancies = []
        for i in range(len(data_vacancies)):
            if self.filter_row(data_vacancies[i], filter_arg):
                data_row = data_vacancies[i]
                vacancies.append(data_row)
        if len(vacancies) == 0:
            return 'Ничего не найдено'
        vacancies = self.sort_table(vacancies)
        return vacancies

    def get_table(self, set_vacancies):
        correct = self.input_correct()
        if correct != 0:
            return correct

        data_vacancies = set_vacancies.vacancies_objects
        if data_vacancies == 'Пустой файл':
            return 'Пустой файл'
        if len(data_vacancies) == 0:
            return 'Нет данных'

        data_vacancies = self.work_vacancies(data_vacancies)

        if data_vacancies == 'Ничего не найдено':
            return 'Ничего не найдено'
        mytable = prettytable.PrettyTable()
        mytable.hrules = prettytable.ALL
        mytable.align = 'l'
        mytable.field_names = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия',
                               'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии']
        mytable.max_width = 20
        for i in data_vacancies:
            mytable.add_row(i.get_row())
        mytable.add_autoindex('№')
        if self.end is None:
            self.end = len(mytable.rows)
        if len(self.fields) == 0:
            return mytable.get_string(start=self.start, end=self.end)
        self.fields.append('№')

        return mytable.get_string(start=self.start, end=self.end, fields=self.fields)

    def sort_table(self, table):
        if self.sort_arg == '':
            return table
        if self.reverse_arg == '':
            self.reverse_arg = 'Нет'
        table.sort(key=self.sort_keys[self.sort_arg], reverse={'Нет': False, 'Да': True}[self.reverse_arg])
        return table

    def filter_row(self, vacancy, filter_argument):
        if filter_argument == '':
            return True
        filter_argument = filter_argument.split(': ')
        if self.filter_fields[filter_argument[0]](vacancy, filter_argument[1]):
            return True
        return False


filename = input('Введите название файла: ')
filter_arg = input('Введите параметр фильтрации: ')
sort_arg = input('Введите параметр сортировки: ')
reverse_arg = input('Обратный порядок сортировки (Да / Нет): ')
limit = input('Введите диапазон вывода: ').split()
fields = input('Введите требуемые столбцы: ')

data_set = DataSet(filename)
user_input = InputConnect(filename, filter_arg, sort_arg, reverse_arg, limit, fields)
print(user_input.get_table(data_set))
