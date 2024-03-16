import socket
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = '/tmp/socket_file'
print('connectiong to {}'.format(server_address))

try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    message = b'Sending a message to server side'
    sock.sendall(message)
    sock.settimeout(2)

    try:
        while True:
            data = str(sock.recv(32))

            if data:
                print('Server response:', data)
            else:
                break
    # 2秒間サーバからの応答がなければ、タイムアウトエラーとなり、エラーメッセージを表示します。
    except(TimeoutError):
        print('Socket timeout, ending listening for server messages')
finally:
    print('closing socket')
    sock.close()
