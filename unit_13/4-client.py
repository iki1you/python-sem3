import socket
import json


def send_request(data):
    host = "127.0.0.32"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    data_string = json.dumps(data)
    client_socket.sendall(data_string.encode())

    response = client_socket.recv(1024).decode()
    client_socket.close()

    return response


data = {
    "command": "get_data",
    "operation": "get_website",
    "name": "Bauer-Weiss"
}

response_str = send_request(data)
response_data = json.loads(response_str)
result = response_data.get("result")

print("Результат:", result)