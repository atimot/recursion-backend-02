import threading
import socket
import sys
import os

from header import Header


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = input("Type in the server's address to connect to: ")
server_port = 9001

try:
    sock.connect((server_address, server_port))
except socket.error as err:
    print(err)
    sys.exit(1)

user_name = input(f"Please enter your username: ")
user_name_len = len(user_name.encode())

operation = int(input(f"Choose to create(1) or join(2) a room: "))

room_name = input(f"Please enter the name of the room you would like: ")
room_name_len = len(room_name.encode())

try:
    # リクエスト送信
    header = Header.protocol_header(room_name_len, operation, Header.STATE_REQUESTED, user_name_len)
    body = room_name + user_name
    sock.send(header)
    sock.send(body.encode())

    # 受信レスポンス確認
    recieved_header = Header(sock.recv(32))
    room_name = sock.recv(recieved_header.room_name_size).decode()
    response = sock.recv(recieved_header.operation_payload_size).decode()

    if response == "NG":
        print(f"server response {response}.")
        sys.exit(1)
    
    recieved_header = Header(sock.recv(32))
    room_name = sock.recv(recieved_header.room_name_size).decode()
    response = sock.recv(recieved_header.operation_payload_size).decode()

    print(f"server response {response}")
finally:
    print("closing socket")
    sock.close()
