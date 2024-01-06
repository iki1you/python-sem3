from xmlrpc.server import SimpleXMLRPCServer
import pandas as pd


class MyServer(SimpleXMLRPCServer):
    def serve_forever(self):
        self.quit = 0
        while not self.quit:
            self.handle_request()


def start_server():
    server = MyServer(('localhost', 8000))
    vacancies = (pd.read_csv('vacancies.csv', encoding='utf8', names=[
        'Название вакансии', 'Зарплата от', 'Зарплата до', 'currency', 'Город', 'published_at'])
                 .loc[:, ['Название вакансии', 'Зарплата от', 'Зарплата до', 'Город']])
    vacancies.index = vacancies.index.astype(str)
    server.register_introspection_functions()

    def get_vacancy_by_id(vac_id):
        return vacancies.iloc[vac_id].to_dict()

    def get_vacancies_by_city(city):
        return str((vacancies[vacancies['Город'].str.contains(city, case=False, na=False)]).T.to_dict('dict'))

    def get_vacancies_by_min_salary(salary):
        return str((vacancies[vacancies['Зарплата от'] >= salary]).T.to_dict('dict'))

    def kill():
        server.quit = 1
        return 1

    server.register_function(get_vacancy_by_id, 'get_vacancy_by_id')
    server.register_function(get_vacancies_by_city, 'get_vacancies_by_city')
    server.register_function(get_vacancies_by_min_salary, 'get_vacancies_by_min_salary')
    server.register_function(kill, 'exit')
    server.serve_forever()


start_server()
