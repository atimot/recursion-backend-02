import threading
import socket

def protocol_data(username_length: int):
    return username_length.to_bytes(1, "big")

server_address = input("type in the server's address to connect to: ")
server_port = 9001

address = ""
port = 9050
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((address, port))

username = input("type in the your user name: ")
username_length = len(username.encode("utf-8"))

# メッセージを受信する関数
def recieve_message():
    while True:
        data, _ = sock.recvfrom(4096)
        
        # 文字出力
        username_length = int.from_bytes(data[:1], "big")
        username = data[1:username_length].decode()
        message = data[1 + username_length:].decode()

        print(f"[{username}] {message}")

# 別スレッドでメッセージを受信する
recieve_thread = threading.Thread(target=recieve_message, daemon=True)
recieve_thread.start()

# メインスレッドではメッセージの入力受付と送信を行う
print("ok. client is alredy!")
try:
    while True:
        message = input()
        send_data = protocol_data(username_length) + (username + message).encode("utf-8")
        sent = sock.sendto(send_data, (server_address, server_port))
finally:
    print("closing socket")
    sock.close()



