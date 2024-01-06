import re
import pandas as pd
import sqlite3


def get_medium(x):
    if x['salary_from'].equals(x['salary_to']):
        return x['salary_from']
    return (x['salary_from'] + x['salary_to']) / 2


def change_data_format(s):
    return re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}', s)[0][:7]


def change_published_data(s):
    a = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}', s)[0]
    return a[:-2] + ':' + a[-2:]


def to_rub(salary, currency, published_at):
    if currency not in ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS']:
        return salary
    cursor = conn.cursor()
    cursor.execute(f"""SELECT {currency} FROM {currency_table} WHERE date = '{change_data_format(published_at)}';""")
    try:
        coef = cursor.fetchall()[0][0]
    except:
        coef = 1
    cursor.close()
    if pd.isna(coef):
        return pd.NA
    return int(salary * coef)


database_name = input()
csv_file = input()
table_name = input()
currency_table = input()

conn = sqlite3.connect(database_name)
vacancies = (pd.read_csv(csv_file, encoding='utf8')
             .assign(salary_from=lambda x: x['salary_from'].fillna(x['salary_to']))
             .assign(salary_to=lambda x: x['salary_to'].fillna(x['salary_from']))
             .assign(salary=get_medium))

for i in vacancies.itertuples():
    vacancies.loc[i.Index, 'salary'] = to_rub(i.salary, i.salary_currency, i.published_at)
    vacancies.loc[i.Index, 'published_at'] = change_published_data(vacancies.loc[i.Index, 'published_at'])
vacancies = (vacancies
    .loc[:, ['name', 'salary', 'area_name', 'published_at']]
    .to_sql(table_name, conn, index=False))
conn.commit()
conn.close()
