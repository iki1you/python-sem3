import math


def get_scale(count, scales):
    if 5 <= count % 100 <= 19 or count % 10 >= 5 or count % 10 == 0:
        return scales[0]
    if count % 10 == 1:
        return scales[1]
    return scales[2]


def translate(string, scales):
    count = int(string.split()[-1])
    if string.split()[1] == 'опыт':
        return string + ' ' + get_scale(count, scales)
    return string + ' ' + get_scale(count, scales)


def empty_filter(string):
    return string if string != '' else False


def int_filter(string):
    return int(string) if str(string).isnumeric() else False


def bool_filter(string):
    return years_info[string] if string in years_info else False


years_info = {'да': True, 'нет': False,
              True: 'да', False: 'нет'}

input_task = [('Введите название вакансии:', empty_filter),
              ('Введите описание вакансии:', empty_filter),
              ('Введите требуемый опыт работы (лет):', int_filter),
              ('Введите нижнюю границу оклада вакансии:', int_filter),
              ('Введите верхнюю границу оклада вакансии:', int_filter),
              ('Есть ли свободный график (да / нет):', bool_filter),
              ('Является ли данная вакансия премиум-вакансией (да / нет):', bool_filter)]

data = []
for i, check in input_task:
    print(i, end=' ')
    line = check(input())
    while not line:
        print('Данные некорректны, повторите ввод')
        print(i, end=' ')
        line = check(input())
    data.append(line)

medium_salary = math.floor((int(data[3]) + int(data[4])) / 2)

output = [f'{data[0]}',
          f'Описание: {data[1]}',
          translate(f'Требуемый опыт работы: {data[2]}', ['лет', 'год', 'года']),
          translate(f'Средний оклад: {medium_salary}', ['рублей', 'рубль', 'рубля']),
          f'Свободный график: {years_info[data[5]]}',
          f'Премиум-вакансия: {years_info[data[6]]}']

print(*output, sep='\n')

