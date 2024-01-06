import socket
import pandas as pd


def start_server():
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
        message = (organizations[organizations['Name']
                         .str.contains(message, case=False, na=False)]['Website'].tolist())[0]
        client.send(message.encode())
