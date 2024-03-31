import socket

def protocol_data(username_length: int):
    return username_length.to_bytes(1, "big")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = input("type in the server's address to connect to: ")
server_port = 9001

username = input("type in the your user name: ")
username_length = len(username.encode("utf-8"))

address = ""
port = 9050
sock.bind((address, port))

print("ok. client is alredy!")
try:
    while True:
        message = input()
        send_data = protocol_data(username_length) + (username + message).encode("utf-8")
        sent = sock.sendto(send_data, (server_address, server_port))

finally:
    print("closing socket")
    sock.close()
