import socket
import json

import pandas as pd


def start_server():
    func_dict = {
        'get_website': 'Website',
        'get_country': 'Country',
        'get_number_of_employees': 'Number of employees'
    }

    host = "127.0.0.32"
    port = 12345
    organizations = pd.read_csv('organizations.csv')
    server = socket.socket()
    server.bind((host, port))
    server.listen(5)
    client, _ = server.accept()

    while True:
        data = client.recv(1024)
        message = data.decode()
        if message == 'exit':
            client.close()
            break
        if message != '':
            message = json.loads(message)
            operation, name = message['operation'], message['name']
            message = (organizations[organizations['Name']
             .str.contains(name, case=False, na=False)][func_dict[operation]].tolist())[0]
            message = json.dumps({'result': message})
            client.send(message.encode())


start_server()