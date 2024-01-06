import socket


def start_client():
    host = "127.0.0.32"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input() # Сюда подается имя организации из organizations.csv
        if message == "exit":
            break
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024).decode()
        print(data)

    client_socket.close()


if __name__ == "__main__":
    start_client()