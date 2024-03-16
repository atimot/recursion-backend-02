import socket
import os

server_address = '/tmp/udp_socket_file'
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
address = '/tmp/udp_client_socket_file'
try:
    os.unlink(address)
except FileNotFoundError:
    # ファイルが存在しない場合は何もしない
    pass
sock.bind(address)

try:
    message = b'Message to send to the client.'
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, server_address)

    print('waiting to receive')
    data, server_address = sock.recvfrom(4096)
    print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close

