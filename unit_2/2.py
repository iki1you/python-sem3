years_info = {'да': True, 'нет': False}
messages = ['Введите название вакансии:',
            'Введите описание вакансии:',
            'Введите требуемый опыт работы (лет):',
            'Введите нижнюю границу оклада вакансии:',
            'Введите верхнюю границу оклада вакансии:',
            'Есть ли свободный график (да / нет):',
            'Является ли данная вакансия премиум-вакансией (да / нет):']

print(*messages)
name = str(input())
description = str(input())
years = int(input())
bottom_salary = int(input())
top_salary = int(input())
is_flexible_hours = years_info[input()]
is_premium = years_info[input()]

for i in [name, description, years, bottom_salary, top_salary, is_flexible_hours, is_premium]:
    print(f'{i} ({type(i).__name__})')