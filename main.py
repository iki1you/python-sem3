import math

while True:
    vacancy_title = input("Введите название вакансии: ")
    if vacancy_title != "" and vacancy_title == 'Программист':
        break
    else:
        print("Данные некорректны, повторите ввод")

while True:
    print("Введите описание вакансии: ")
    vacancy_description = input()
    if vacancy_description != "" and vacancy_description == 'Хорошие знания C#, JavaScript(Опыт работы. Синтаксис. ООП)':
        break
    else:
        print("Данные некорректны, повторите ввод")

while True:
    required_experience = input("Введите требуемый опыт работы (лет): ")
    if required_experience != '' and required_experience.isdigit():
        break
    else:
        print("Данные некорректны, повторите ввод")

while True:
    lower_salary_limit = input("Введите нижнюю границу оклада вакансии: ")
    if lower_salary_limit != '' and lower_salary_limit.isdigit():
        break
    else:
        print("Данные некорректны, повторите ввод")

while True:
    upper_salary_limit = input("Введите верхнюю границу оклада вакансии: ")
    if upper_salary_limit != '' and upper_salary_limit.isdigit():
        break
    else:
        print("Данные некорректны, повторите ввод")

while True:
    flexible_schedule = input("Есть ли свободный график (да / нет): ")
    if flexible_schedule != '' and (flexible_schedule.lower() == "да" or flexible_schedule.lower() == "нет"):
        break
    else:
        print("Данные некорректны, повторите ввод.")

while True:
    premium_vacancy = input("Является ли данная вакансия премиум-вакансией (да / нет): ")
    if premium_vacancy != '' and (premium_vacancy.lower() == "да" or premium_vacancy.lower() == "нет"):
        break
    else:
        print("Данные некорректны, повторите ввод.")

middle_salary = math.floor((int(upper_salary_limit) + int(lower_salary_limit))/2)

print(vacancy_title)
print("Описание:", vacancy_description)
if int(required_experience) == 1:
    print("Требуемый опыт работы:",required_experience, "год")
elif int(required_experience) > 1 and int(required_experience) < 5:
    print("Требуемый опыт работы:", required_experience, "года")
else:
    print("Требуемый опыт работы:", required_experience, "лет")
if middle_salary == 2:
    print("Средний оклад:", middle_salary, "рубля")
else:
    print("Средний оклад:", middle_salary, "рублей")
print("Свободный график: "+ flexible_schedule)
print("Премиум-вакансия: "+ premium_vacancy)