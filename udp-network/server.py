import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
server_port = 9001
print(f"starting up on port {server_port}")

sock.bind((server_address, server_port))

while True:
    print("\nwaiting to receive message")
    data, address = sock.recvfrom(4096)

    print(f"receved {len(data)} bytes from {address}")
    print(data)

    if data:
        sent = sock.sendto(data, address)
        print(f"sent {sent} bytes back to {address}")

