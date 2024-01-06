import pandas as pd


def get_medium(x):
    if x['salary_from'].equals(x['salary_to']):
        return x['salary_from']
    return (x['salary_from'] + x['salary_to']) / 2


vacancies = dict((pd.read_csv('vacancies.csv')
    .assign(salary_from=lambda x: x['salary_from'].fillna(x['salary_to']))
    .assign(salary_to=lambda x: x['salary_to'].fillna(x['salary_from']))
    .assign(medium_salary=get_medium).groupby(['area_name']).agg({'medium_salary': 'mean'})
    .sort_values(['medium_salary', 'area_name'], ascending=(False, True))['medium_salary']))
print(vacancies)
