import math


def choose_years(count):
    if count == 1:
        return 'год'
    elif count in range(2, 5):
        return 'года'
    return 'лет'


def choose_rubles(count):
    if 5 <= count % 100 <= 19 or count % 10 >= 5 or count % 10 == 0:
        return 'рублей'
    if count % 10 == 1:
        return 'рубль'
    return 'рубля'


def translate(line):
    count = int(line.split()[-1])
    if line.split()[1] == 'опыт':
        return line + ' ' + choose_years(count)
    return line + ' ' + choose_rubles(count)


years_info = {'да': True, 'нет': False,
              True: 'да', False: 'нет'}

input_task = ['Введите название вакансии:',
              'Введите описание вакансии:',
              'Введите требуемый опыт работы (лет):',
              'Введите нижнюю границу оклада вакансии:',
              'Введите верхнюю границу оклада вакансии:',
              'Есть ли свободный график (да / нет):',
              'Является ли данная вакансия премиум-вакансией (да / нет):']

print(*input_task, sep=' ', end=' ')

name = str(input())
description = str(input())
years = int(input())
bottom_salary = int(input())
top_salary = int(input())
is_flexible_hours = years_info[input()]
is_premium = years_info[input()]

medium_salary = math.floor((int(bottom_salary) + int(top_salary)) / 2)

output = [f'{name}',
          f'Описание: {description}',
          translate(f'Требуемый опыт работы: {years}'),
          translate(f'Средний оклад: {medium_salary}'),
          f'Свободный график: {years_info[is_flexible_hours]}',
          f'Премиум-вакансия: {years_info[is_premium]}']

print(*output, sep='\n')
