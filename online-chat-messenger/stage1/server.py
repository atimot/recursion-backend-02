import socket
from datetime import datetime, timedelta
import time
import threading

# IPv4、UDPでソケット作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = "0.0.0.0"
server_port = 9001
sock.bind((server_address, server_port))

clients:dict = {}
clients_lock = threading.Lock()

# クライアントのクリーンアップを行う関数
def cleanup_clients():
    while True:
        now = datetime.now()

        with clients_lock:
            keys_to_remove = [key for key, value in clients.items() if now - value['last_recived'] > timedelta(minutes=1)]
            for key in keys_to_remove:
                del clients[key]
        print("cleanuped clients now.")
        time.sleep(60)

# クリーンアップスレッドを開始
cleanup_thread = threading.Thread(target=cleanup_clients, daemon=True)
cleanup_thread.start()

print(f"starting server at {server_address, server_port}")
while True:
    data, address = sock.recvfrom(4096)
    print(int.from_bytes(data[:1], "big"))
    print(data[1:].decode())
    
    # 最終受信時刻を記録
    with clients_lock:
        clients[address] = {
            "last_recived": datetime.now()
        }

    with clients_lock:
        for key, _ in clients.items():
            # 自分以外に送信
            if address != key:
                sock.sendto(data, key)
