import re

import pandas as pd


def get_medium(x):
    if x['salary_from'].equals(x['salary_to']):
        return x['salary_from']
    return (x['salary_from'] + x['salary_to']) / 2


def get_vac_by_city(data):
    k = data.shape[0]
    d = (data.groupby(['area_name']).agg({
        'count': 'count',
        'medium_salary': 'mean'
    })
         .assign(count=lambda x: round(x['count'] / k, 4))
         .query('count >= 0.01')
         .astype({'medium_salary': 'int'}))
    return (d.sort_values(['medium_salary', 'area_name'], ascending=(False, True))[:10].to_dict()['medium_salary'],
            d.sort_values(['count', 'area_name'], ascending=(False, True))[:10].to_dict()['count'])


def get_vac_by_years(data):
    d = data.groupby(['published_at']).agg({
        'count': 'count',
        'medium_salary': 'mean'
    }).astype({'medium_salary': 'int'}).to_dict()
    salary = d['medium_salary']
    y_count = d['count']
    for i in range(2017, 2024):
        if i not in salary:
            salary[i] = 0
        if i not in y_count:
            y_count[i] = 0
    return dict(sorted(salary.items(), key=lambda x: x[0])), dict(sorted(y_count.items(), key=lambda x: x[0]))


def get_year_vacancy(s):
    for j in re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}', s):
        s = s.replace(j, j[0:4])
    return int(s)


def print_data(name_vac, name_file):
    vacancies = (pd.read_csv(name_file)
                 .assign(salary_from=lambda x: x['salary_from'].fillna(x['salary_to']))
                 .assign(salary_to=lambda x: x['salary_to'].fillna(x['salary_from']))
                 .assign(published_at=lambda x: x['published_at'].apply(get_year_vacancy))
                 .assign(count=0)
                 .assign(medium_salary=get_medium))
    level_sal, count_sal = get_vac_by_years(vacancies)
    print(f'Динамика уровня зарплат по годам: {level_sal}')
    print(f'Динамика количества вакансий по годам: {count_sal}')
    vacancies = vacancies[vacancies['name'].str.contains(name_vac, na=False, case=False)]
    level_sal_job, count_sal_job = get_vac_by_years(vacancies)
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {level_sal_job}')
    print(f'Динамика количества вакансий по годам для выбранной профессии: {count_sal_job}')
    level_sal_city, count_sal_city = get_vac_by_city(vacancies)
    print(f'Уровень зарплат по городам (в порядке убывания): {level_sal_city}')
    print(f'Доля вакансий по городам (в порядке убывания): {count_sal_city}')


file_name = 'vacancies_for_learn.csv'
vac_name = input()

print_data(vac_name, file_name)
