import xmlrpc.client


client = xmlrpc.client.ServerProxy('http://localhost:8000')
while True:
    command = input()

    if command == 'exit':
        method = getattr(client, command)
        method()
        break

    command = command.split()
    method_name = command[0]
    method_value = command[1]

    method = getattr(client, command[0])
    if method_name == 'get_vacancy_by_id':
        result = method(int(method_value))
        print(result)
    elif method_name == 'get_vacancies_by_city':
        result = method(str(method_value))
        print(result)
    elif method_name == 'get_vacancies_by_min_salary':
        result = method(int(method_value))
        print(result)