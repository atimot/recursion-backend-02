import socket
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = "/tmp/socket_file"


try:
    print(f"connecting to {server_address}")
    sock.connect(server_address)
    print(f"connected to {server_address}")
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    print("type the message you want to send")
    message = input()
    sock.sendall(message)
    sock.settimeout(2)

    try:
        while True:
            data = str(sock.recv(32))

            if data:
                print(f"<<server response>>: {data}")
            else:
                break
    except TimeoutError:
        print("socket timeout, ending listening for server message")
finally:
    print("closing socket")
    sock.close()
