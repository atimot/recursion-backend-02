import socket
import os

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = "/tmp/socket_file"

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
            print(f"<<recieved>>: {data_str}")

            if data:
                response = f"processing: {data_str}"
                connection.sendall(response.encode())
            else:
                print(f"no data from {client_address}")
                break
    finally:
        print("closing current connection")
        connection.close()
