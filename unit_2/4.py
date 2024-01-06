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


def translate(string):
    count = int(string.split()[-1])
    if string.split()[1] == 'опыт':
        return string + ' ' + choose_years(count)
    return string + ' ' + choose_rubles(count)


def empty_check(string):
    return string != ''


def int_check(string):
    return str(string).isnumeric()


def bool_check(string):
    return string in years_info


def input_filter(checker, task):
    print(task, end=' ')
    string = input()
    while not checker(string):
        print('Данные некорректны, повторите ввод')
        print(task, end=' ')
        string = input()
    return string


years_info = {'да': True, 'нет': False,
              True: 'да', False: 'нет'}

name = str(input_filter(empty_check, 'Введите название вакансии:'))
description = str(input_filter(empty_check, 'Введите описание вакансии:'))
years = int(input_filter(int_check, 'Введите требуемый опыт работы (лет):'))
bottom_salary = int(input_filter(int_check, 'Введите нижнюю границу оклада вакансии:'))
top_salary = int(input_filter(int_check, 'Введите верхнюю границу оклада вакансии:'))
is_flexible_hours = bool(years_info[input_filter(bool_check, 'Есть ли свободный график (да / нет):')])
is_premium = bool(years_info[input_filter(bool_check, 'Является ли данная вакансия премиум-вакансией (да / нет):')])

medium_salary = math.floor((int(bottom_salary) + int(top_salary)) / 2)

output = [f'{name}',
          f'Описание: {description}',
          translate(f'Требуемый опыт работы: {years}'),
          translate(f'Средний оклад: {medium_salary}'),
          f'Свободный график: {years_info[is_flexible_hours]}',
          f'Премиум-вакансия: {years_info[is_premium]}']

print(*output, sep='\n')