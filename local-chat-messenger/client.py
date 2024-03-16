import socket
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = "/tmp/socket_file"


try:
    print(f"connecting to {server_address}")
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    print("type the message you want to send")
    message = input()
    sock.sendall(message.encode())
    sock.settimeout(2)

    try:
        while True:
            data = sock.recv(32).decode()

            if data:
                print(f"{{res}}: {data}")
            else:
                break
    except TimeoutError:
        print("socket timeout, ending listening for server message")
finally:
    print("closing socket")
    sock.close()
