import socket

host = "127.0.0.32"
port = 12345
client = socket.socket()
client.connect((host, port))
message = "Hello!"
client.send(message.encode())
client.close()