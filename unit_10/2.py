import pandas as pd
from collections import Counter


def update_counter(x):
    if isinstance(x, str):
        x = x.replace('\r', '')
        return counter.update(Counter(x.strip().split('\n')))


vacancies = pd.read_csv('vacancies_small.csv')
name = input()
counter = Counter()
vacancies = vacancies[vacancies['name'].str.contains(name, case=False, na=False)]
vacancies['key_skills'].apply(update_counter)
print(list(dict(counter.most_common(5)).items()))
