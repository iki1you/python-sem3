import csv
import math
import re


def drop_tags(s, count_repl=1):
    if count_repl == 0:
        return s
    return drop_tags(*re.subn(r'<[^<>]*>', '', s))


def parse_data(data):
    a = data[0].index('salary_currency')
    rows = list(filter(lambda x: (x[a] == 'RUR' and len(x) == len(data[0]) and all([len(e) > 0 for e in x])), data[1:]))
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            rows[i][j] = drop_tags(rows[i][j])
    return [dict((x, y) for (x, y) in zip(data[0], rows[i])) for i in range(len(rows))]


def parse_top_skills(data):
    vacancies = []
    skills = dict()
    for row in data:
        if '\n' in row['key_skills']:
            ans = []
            for s in row['key_skills'].split('\n'):
                ans.append(s)
                if s in skills:
                    skills[s] += 1
                else:
                    skills[s] = 1
        else:
            if row['key_skills'] in skills:
                skills[row['key_skills']] += 1
            else:
                skills[row['key_skills']] = 1
        vacancies.append(skills)
    return dict(sorted(skills.items(), key=lambda x: x[1], reverse=True))


def choose_times(count):
    if 5 <= count % 100 <= 19 or count % 10 >= 5 or count % 10 == 0:
        return f'{count} раз'
    if count % 10 == 1:
        return f'{count} раз'
    return f'{count} раза'


def choose_rubles(count):
    count = int(count)
    if 5 <= count % 100 <= 19 or count % 10 >= 5 or count % 10 == 0:
        return 'рублей'
    if count % 10 == 1:
        return 'рубль'
    return 'рубля'


def choose_vacancy(count):
    if 5 <= count % 100 <= 19 or count % 10 >= 5 or count % 10 == 0:
        return 'вакансий'
    elif count % 10 == 1:
        return 'вакансия'
    return 'вакансии'


def choose_cities(count):
    if count % 10 == 1:
        return 'города'
    return 'городов'


def get_top_skills(skills):
    skills = parse_top_skills(skills)
    output = [f'Из {len(skills)} скиллов, самыми популярными являются:']
    for (i, skill) in enumerate(skills):
        if i == 10:
            break
        skill = skill.strip()
        output.append(f'    {i + 1}) {skill} - упоминается {choose_times(skills[skill])}')
    return '\n'.join(output)


def parse_average_salary(data):
    salary = dict()
    for i in data:
        if i['area_name'] in get_white_cities(data):
            if i['area_name'] not in salary:
                salary[i['area_name']] = [(float(i['salary_from']) + float(i['salary_to'])) / 2]
            else:
                salary[i['area_name']].append(((float(i['salary_from']) + float(i['salary_to'])) / 2))
    salary = dict(sorted(
        [(i, salary[i]) for i in salary], key=lambda x: (sum(x[1]) / len(x[1])), reverse=True))
    return salary


def get_top_cities(data):
    top_cities = parse_average_salary(data)
    count_cities = len(top_cities)
    output = [f'Из {count_cities} {choose_cities(count_cities)}, самые высокие средние ЗП:']
    for (i, key) in enumerate(top_cities):
        if i == 10:
            break
        salary = int(sum(top_cities[key]) / len(top_cities[key]))
        count = len(top_cities[key])
        output.append(
            f'    {i + 1}) {key} - средняя зарплата {salary} '
            f'{choose_rubles(salary)} ({count} {choose_vacancy(count)})'
        )
    return '\n'.join(output)


def sort_average_salary(data, sort_reverse):
    return sorted(data, key=lambda x: (float(x['salary_from']) + float(x['salary_to'])) / 2,
                  reverse=sort_reverse)


def get_salary_list(value):
    output = []
    salary_list = srt_sal[:10]
    if value == 'top':
        output.append('Самые высокие зарплаты:')
    else:
        salary_list = sorted(srt_sal[-10:][::-1], key=lambda x: x['area_name'])
        print(salary_list)
        output.append('Самые низкие зарплаты:')
    for (i, vacancy) in enumerate(salary_list):
        salary = math.floor((float(vacancy['salary_to']) + float(vacancy['salary_from'])) / 2)
        output.append(
            f'    {i + 1}) {vacancy["name"]} в компании "{vacancy["employer_name"]}" - '
            f'{salary} {choose_rubles(salary)} (г. {vacancy["area_name"]})'
        )
    return '\n'.join(output)


def get_white_cities(data):
    cities = dict()
    k = 0
    for i in data:
        if i['salary_currency'] == 'RUR':
            k += 1
        if i['area_name'] not in cities:
            cities[i['area_name']] = 1
        else:
            cities[i['area_name']] += 1
    return list(filter(lambda x: (cities[x] / k * 100) >= 1, cities))


def parse_for_cities(data, cities):
    return list(filter(lambda x: x['area_name'] in cities, data))


def print_analytics(data):
    print(get_salary_list('top'))
    print()
    print(get_salary_list('bottom'))
    print()
    print(get_top_skills(data))
    print()
    print(get_top_cities(data))


# example_vacancies.csv
filename = input()
with open(filename, encoding='utf-8-sig') as file:
    raw = [i for i in csv.reader(file)]
    parsed_data = parse_data(raw)
    srt_sal = sort_average_salary(parsed_data, True)

print_analytics(parsed_data)

