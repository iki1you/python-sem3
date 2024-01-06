import csv
import math
import re


def drop_extra_spaces(line):
    return ' '.join(filter(lambda x: not x.isspace(), ', '.join([i.strip() for i in line.split('\n')]).split()))


def drop_tags(line):
    return re.sub(r'<.*?>', '', line)


def parse_data(data):
    headers = list(data[0])
    rows = list(filter(lambda x: len(x) == len(headers), filter(lambda x: all([len(e) > 0 for e in x]), data[1:])))
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = drop_extra_spaces(drop_tags(rows[i][j]))
    return [dict((x, y) for (x, y) in zip(headers, rows[i])) for i in range(len(rows))]

def filter_currency(data):
    return list(filter(lambda x: x['salary_currency'] == 'RUR', data))


def parse_top_skills(data):
    skills = dict()
    for i in data:
        for item in i['key_skills'].split(', '):
            if item not in skills:
                skills[item] = 1
            else:
                skills[item] += 1
    return dict(sorted(skills.items(), key=lambda x: x[1], reverse=True))


def choose_times(count):
    if count % 10 in [2, 3, 4] and count % 100 != 1:
        return f'{count} раза'
    return f'{count} раз'


def get_top_skills(data):
    skills = parse_top_skills(data)
    output = [f'Из {len(skills)} скиллов, самыми популярными являются:']
    for (i, skill) in enumerate(skills):

        skill = skill.strip()
        output.append(f'    {i + 1}) {skill} - упоминается {choose_times(skills[skill])}')
    return '\n'.join(output)


def parse_average_salary(data):
    average_salary = dict()
    for i in data:
        if i['area_name'] not in average_salary:
            average_salary[i['area_name']] = [(int(i['salary_from']) + int(i['salary_to'])) / 2]
        else:
            average_salary[i['area_name']].append((int(i['salary_from']) + int(i['salary_to'])) / 2)
    average_salary = dict(sorted(
        [(i, average_salary[i]) for i in average_salary], key=lambda x: math.floor(sum(x[1]) / len(x[1])),
        reverse=True))
    return average_salary


def choose_rubles(count):
    count = int(count)
    if 5 <= count % 100 <= 19 or count % 10 >= 5 or count % 10 == 0:
        return 'рублей'
    if count % 10 == 1:
        return 'рубль'
    return 'рубля'


def choose_vacancy(count):
    if count % 10 in [2, 3, 4] and count % 100 != 1:
        return 'вакансии'
    elif count % 10 == 1:
        return 'вакансия'
    return 'вакансий'


def choose_cities(count):
    if count % 10 == 1:
        return 'города'
    return 'городов'


def get_top_cities(data):
    top_cities = parse_average_salary(data)
    count_cities = len(top_cities)
    output = [f'Из {count_cities} {choose_cities(count_cities)}, самые высокие средние ЗП:']
    for (i, key) in enumerate(top_cities):
        if i == 10:
            break
        salary = math.floor(sum(top_cities[key]) / len(top_cities[key]))
        count = len(top_cities[key])
        output.append(
            f'    {i + 1}) {key} - средняя зарплата {salary} '
            f'{choose_rubles(salary)} ({count} {choose_vacancy(count)})'
        )
    return '\n'.join(output)


def sort_average_salary(data, sort_reverse):
    return sorted(data, key=lambda x: math.floor((int(x['salary_from']) + int(x['salary_to'])) / 2),
                  reverse=sort_reverse)[:10]


def get_salary_list(data, value):
    output = []
    if value == 'top':
        data = sort_average_salary(data, True)
        output.append('Самые высокие зарплаты:')
    else:
        data = sort_average_salary(data, False)
        output.append('Самые низкие зарплаты:')
    for (i, vacancy) in enumerate(data):
        salary = math.floor((int(vacancy['salary_from']) + int(vacancy['salary_to'])) / 2)
        output.append(
            f'    {i + 1}) {vacancy["name"]} в компании "{vacancy["employer_name"]}" - '
            f'{salary} {choose_rubles(salary)} (г. {vacancy["area_name"]})'
        )
    return '\n'.join(output)





def parse_for_cities(data, cities):
    return list(filter(lambda x: x['area_name'] in cities, data))


def print_analytics(data):
    print(get_salary_list(data, 'top'))
    print()
    print(get_salary_list(data, 'bottom'))
    print()
    print(get_top_skills(data))
    print()
    print(get_top_cities(data))


# example_vacancies.csv
# filename = input()
# with open(filename, encoding='utf-8-sig') as file:
    # parsed_data = filter_currency(parse_data([i for i in csv.reader(file)]))
    # parsed_data = parse_for_cities(parsed_data, get_white_cities(parsed_data))

# print_analytics(parsed_data)

def get_cities(data):
    cities = dict()
    k = 0
    for i in data:
        k += 1
        if i['area_name'] not in cities:
            cities[i['area_name']] = 1
        else:
            cities[i['area_name']] += 1
    for x, y in cities.items():
        print(x, y, y / 347 * 100)
    print(k)
    return list(filter(lambda x: math.floor(cities[x] / 347 * 100) >= 1, cities))


def parse_data2(data):
    headers = list(data[0])
    rows = list(filter(lambda x: len(x) == len(headers), filter(lambda x: all([len(e) > 0 for e in x]), data[1:])))
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = drop_tags(rows[i][j])
    return [dict((x, y) for (x, y) in zip(headers, rows[i])) for i in range(len(rows))]


def filter_data(data):
    data = filter_currency(filter(lambda x: len(x) == len(data[0]),
                                  filter(lambda x: all([len(e) > 0 for e in x]), data)))
    return data


def get_white_cities(data):
    cities = dict()
    for i in data:
        if i['area_name'] not in cities:
            cities[i['area_name']] = 1
        else:
            cities[i['area_name']] += 1
    return list(filter(lambda x: math.ceil(cities[x] / len(data) * 100) >= 1, cities))

import test
test_data = test.test_data
parsed_data = parse_data2(test_data)
parsed_data = parse_for_cities(parsed_data, get_white_cities(parsed_data))
print_analytics(filter_data(parsed_data))
print(len(test_data))
