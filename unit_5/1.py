import csv
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


def csv_filer(reader, list_naming):
    vacancies = []
    for i in list_naming:
        vacancy = dict()
        for j, key in enumerate(reader):
            vacancy[key] = drop_extra_spaces(drop_tags(i[j])).strip()
        vacancies.append(vacancy)
    return vacancies


def print_vacancies(data_vacancies, dic_naming):
    for i in range(len(data_vacancies)):
        for key, value in data_vacancies[i].items():
            if key in dic_naming:
                key = dic_naming[key]
            if value == 'True':
                value = 'Да'
            if value == 'False':
                value = 'Нет'
            print(f'{key}: {value}')
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
    'salary_gross': 'Оклад указан до вычета налогов',
    'salary_currency': 'Идентификатор валюты оклада',
    'area_name': 'Название региона',
    'published_at': 'Дата и время публикации вакансии'
}

print_vacancies(csv_filer(*csv_reader(input())), naming)
