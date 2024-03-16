import socket
import os
import sys
from faker import Faker

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = "/tmp/socket_file"
fake = Faker()

if os.path.exists(server_address):
    os.unlink(server_address)

print(f"starting up on {server_address}")
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        print(f"connection from {client_address}")
        while True:
            data = connection.recv(32)
            data_str = data.decode("utf-8")
            print(f"{{recv}}: {data_str}")

            if data:
                response = f"hi! my name is {fake.name()}. my address is {fake.address()}. {fake.text()}"
                connection.sendall(response.encode())
            else:
                print(f"no data from {client_address}")
                break
    finally:
        print("closing current connection")
        connection.close()
