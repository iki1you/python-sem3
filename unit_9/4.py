import csv
import re


class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = self.write_vacancies()

    def write_vacancies(self):
        vacancies = self.csv_parser(self.file_name)
        total = []
        for i in vacancies:
            vacancy = Vacancy(
                i['name'],
                Salary(i['salary_from'], i['salary_to'], i['salary_currency']),
                i['area_name'],
                i['published_at']
            )
            total.append(vacancy)
        return total

    @staticmethod
    def drop_extra_spaces(line):
        s = ''
        for i in line:
            if not (i.isspace() and i != ' ' and i != '\n'):
                s += i
            else:
                s += ' '
        line = s
        while '  ' in line:
            line = line.replace('  ', ' ')
        line = line.strip()
        return line

    @staticmethod
    def drop_tags(line):
        return re.sub(r'<.*?>', '', line)

    @staticmethod
    def csv_parser(file_name):
        def csv_reader(csv_name):
            with open(csv_name, encoding='utf-8-sig') as file:
                data = [i for i in csv.reader(file)]
            return (data[0],
                    list(
                        filter(lambda x: len(x) == len(data[0]),
                               filter(lambda x: all([len(e) > 0 for e in x]), data[1:]))))

        def csv_filer(r, list_naming):
            csv_vacancies = []
            for i in list_naming:
                vacancy = dict()
                for j, key in enumerate(r):
                    vacancy[key] = DataSet.drop_extra_spaces(DataSet.drop_tags(i[j]))
                csv_vacancies.append(vacancy)
            return csv_vacancies

        reader = csv_reader(file_name)
        if reader == 'Пустой файл':
            return 'Пустой файл'
        vacancies = csv_filer(*reader)
        return vacancies


class Vacancy:
    def __init__(self, *args):
        (self.name, self.salary, self.area_name, self.published_at) = args
        self.salary: Salary = self.salary


class Salary:
    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, salary_from, salary_to, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.medium = int((float(self.salary_from) + float(self.salary_to)) /
                          2) * self.currency_to_rub[salary_currency]


class Statistics:
    def __init__(self, vacancies, job_name):
        self.vacancies: list[Vacancy] = vacancies
        self.job_name = job_name
        self.vacancies_by_year = self.get_vacancies_by_year(self.vacancies)
        self.vacancies_by_cities = self.get_vacancies_by_cities()
        self.filtered_vacancies_by_year = self.get_vacancies_by_year(self.get_filtered_by_job())

    def get_filtered_by_job(self):
        vacancies = []
        for i in self.vacancies:
            if self.job_name in i.name:
                vacancies.append(i)
        return vacancies

    def get_vacancies_by_year(self, vacancies):
        years_vacancies = dict()
        for i in vacancies:
            year = self.get_year_vacancy(i.published_at)
            if year not in years_vacancies:
                years_vacancies[year] = [i]
            else:
                years_vacancies[year].append(i)
        return years_vacancies

    def get_vacancies_by_cities(self):
        vacancies_by_area = dict()
        for i in self.vacancies:
            area = i.area_name
            if area not in vacancies_by_area:
                vacancies_by_area[area] = [i]
            else:
                vacancies_by_area[area].append(i)
        total = dict()
        for i in vacancies_by_area:
            if len(vacancies_by_area[i]) / len(self.vacancies) >= 0.01:
                area = i
                if area not in total:
                    total[area] = vacancies_by_area[i]
                else:
                    total[area].append(*vacancies_by_area[i])
        return total

    def get_part_of_vacancies_by_cities(self):
        dynamics = dict()
        for key, i in self.vacancies_by_cities.items():
            dynamics[key] = round(len(i) / len(self.vacancies), 4)
        return dict(sorted(dynamics.items(), key=lambda x: x[1], reverse=True)[:10])

    def dynamics_of_count_vacancies_by_year(self):
        dynamics = dict()
        for key, i in self.vacancies_by_year.items():
            dynamics[key] = len(i)
        return dynamics

    @staticmethod
    def get_year_vacancy(s):
        for j in re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}', s):
            s = s.replace(j, j[0:4])
        return int(s)

    def filtered_count_by_year(self):
        dynamics = dict()
        for key, i in self.filtered_vacancies_by_year.items():
            dynamics[key] = len(i)
        for i in self.vacancies_by_year:
            if i not in dynamics:
                dynamics[i] = 0
        return dynamics

    def dynamics_of_salary_levels_by_year(self):
        dynamics = dict()
        for key, i in self.vacancies_by_year.items():
            dynamics[key] = int(sum([e.salary.medium for e in i]) / len(i))
        return dynamics

    def filtered_levels_by_year(self):
        dynamics = dict()
        for key, i in self.filtered_vacancies_by_year.items():
            dynamics[key] = int(sum([e.salary.medium for e in i]) / len(i))
        for i in self.vacancies_by_year:
            if i not in dynamics:
                dynamics[i] = 0
        return dynamics

    def dynamics_of_salary_by_cities(self):
        dynamics = dict()
        for key, i in self.vacancies_by_cities.items():
            dynamics[key] = int(sum([e.salary.medium for e in i]) / len(i))
        return dict(sorted(dynamics.items(), key=lambda x: x[1], reverse=True)[:10])

    def __str__(self):
        level_salary = self.dynamics_of_salary_levels_by_year()
        count_vacancies = self.dynamics_of_count_vacancies_by_year()
        job_level_salary = self.filtered_levels_by_year()
        job_count_vacancies = self.filtered_count_by_year()
        level_salary_by_cities = self.dynamics_of_salary_by_cities()
        part_of_vacancies_by_cities = self.get_part_of_vacancies_by_cities()
        return (f'Динамика уровня зарплат по годам: {level_salary}\n'
                f'Динамика количества вакансий по годам: {count_vacancies}\n'
                f'Динамика уровня зарплат по годам для выбранной профессии: {job_level_salary}\n'
                f'Динамика количества вакансий по годам для выбранной профессии: {job_count_vacancies}\n'
                f'Уровень зарплат по городам (в порядке убывания): {level_salary_by_cities}\n'
                f'Доля вакансий по городам (в порядке убывания): {part_of_vacancies_by_cities}')


filename = input('Введите название файла: ')
job = input('Введите название профессии: ')

data_set = DataSet(filename)
statistics = Statistics(data_set.vacancies_objects, job)
print(statistics)

# vacancies_for_learn.csv
# Аналитик
