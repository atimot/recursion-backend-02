import socket
from datetime import datetime, timedelta
import time
import threading
from header import Header
from room import Room
from user import User

# clients: dict = {}
rooms: dict[str, Room] = {}
# clients_lock = threading.Lock()

# クライアントのクリーンアップを行う関数
# def cleanup_clients():
#     while True:
#         now = datetime.now()

#         with clients_lock:
#             keys_to_remove = [key for key, value in clients.items() if now - value['last_recived'] > timedelta(minutes=1)]
#             for key in keys_to_remove:
#                 del clients[key]
#         print("cleanuped clients now.")
#         time.sleep(60)

# # クリーンアップスレッドを開始
# cleanup_thread = threading.Thread(target=cleanup_clients, daemon=True)
# cleanup_thread.start()

def generate_token(user_name: str, room_name: str, ip: str):
    """
    ユーザー認証用のトークンを生成する
    """
    return (user_name + room_name + ip).encode().hex()

# TCPコネクションで初回受付を行う
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = "0.0.0.0"
server_port = 9001
sock.bind((server_address, server_port))
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        received_header = Header(connection.recv(32))
        room_name = connection.recv(received_header.room_name_size).decode()
        user_name = connection.recv(received_header.operation_payload_size).decode()
        client_ip, client_port = client_address

        if not received_header.validate():
            response_payload = "NG"
            response_header = Header.protocol_header(
                received_header.room_name_size,
                received_header.operation,
                Header.STATE_CONFORMANCE,
                len(response_payload.encode())
            )
            response_body = (room_name + response_payload).encode()

            connection.send(response_header)
            connection.send(response_body)
            continue

        response_payload = "OK"
        response_header = Header.protocol_header(
            received_header.room_name_size,
            received_header.operation,
            Header.STATE_CONFORMANCE,
            len(response_payload.encode())
        )
        response_body = (room_name + response_payload).encode()

        connection.send(response_header)
        connection.send(response_body)

        # 部屋参加、作成処理
        user = User(user_name, client_ip, client_port)
        token = generate_token(user_name, room_name, client_ip)

        if received_header.operation == Header.ROOM_CREATE:
            room = Room(room_name, user, token)
            rooms[room.get_name()] = room
        elif received_header.operation == Header.ROOM_JOIN:
            room = rooms[room_name]
            room.add_user(user, token)

        response_header = Header.protocol_header(
            received_header.room_name_size,
            received_header.operation,
            Header.STATE_COMPLETE,
            len(token.encode())
        )
        response_body = (room_name + token).encode()

        connection.send(response_header)
        connection.send(response_body)

    finally:
        print(f"client connection closed.")
        connection.close()



# IPv4、UDPでソケット作成
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address = "0.0.0.0"
# server_port = 9001
# sock.bind((server_address, server_port))

# print(f"starting server at {server_address, server_port}")
# while True:
#     data, address = sock.recvfrom(4096)
    
#     # 最終受信時刻を記録
#     with clients_lock:
#         clients[address] = {
#             "last_recived": datetime.now()
#         }

#     with clients_lock:
#         for key, _ in clients.items():
#             # 自分以外に送信
#             if address != key:
#                 sock.sendto(data, key)
