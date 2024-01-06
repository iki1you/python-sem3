from xmlrpc.server import SimpleXMLRPCServer
import pandas as pd

is_run = True


def start_server():
    with SimpleXMLRPCServer(('localhost', 8000)) as server:
        vacancies = (pd.read_csv('vacancies.csv', encoding='utf8', names=[
            'Название вакансии', 'Зарплата от', 'Зарплата до', 'currency', 'Город', 'published_at'])
                     .loc[:, ['Название вакансии', 'Зарплата от', 'Зарплата до', 'Город']])
        vacancies.index = vacancies.index.map(str)
        server.register_introspection_functions()

        def get_vacancy_by_id(vac_id):
            return vacancies.iloc[str(vac_id)].to_dict()

        def get_vacancies_by_city(city):
            return str((vacancies[vacancies['Город'].str.contains(city, case=False, na=False)]).T.to_dict('dict'))

        def get_vacancies_by_min_salary(salary):
            return str((vacancies[vacancies['Зарплата от'] >= salary]).T.to_dict('dict'))

        def exit_server():
            global is_run
            is_run = False
            return 0

        server.register_function(get_vacancy_by_id, 'get_vacancy_by_id')
        server.register_function(get_vacancies_by_city, 'get_vacancies_by_city')
        server.register_function(get_vacancies_by_min_salary, 'get_vacancies_by_min_salary')
        server.register_function(exit_server, 'exit')

        global is_run
        while is_run:
            server.handle_request()



start_server()
