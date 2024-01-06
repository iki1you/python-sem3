import pandas as pd

vacancies = pd.read_csv('vacancies_small.csv')

column = input()
key = input()
sort_by = input()
print(vacancies[vacancies[column]
      .str.contains(key, case=False, na=False)]
      .sort_values(by=sort_by, ascending=False)['name']
      .tolist())
