import socket
import sys
import os

def protocol_header(filename_length: int, json_length: int, data_length: int):
    return filename_length.to_bytes(1, "big") + json_length.to_bytes(3, "big") + data_length.to_bytes(4, "big")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = input("type in the server's address to connecto to: ")
server_port = 9001

print(f"connecting to {(server_address, server_port)}")

try:
    sock.connect((server_address, server_port))
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    filepath = input("type in a file to upload: ")

    with open(filepath, "rb") as f:
        f.seek(0, os.SEEK_END)
        filesize = f.tell()
        f.seek(0, 0)

        if filesize > pow(2, 32):
            raise Exception("file must be below 2GB.")
        
        filename = os.path.basename(f.name)
        filename_bits = filename.encode("utf-8")
        header = protocol_header(len(filename_bits), 0, filesize)

        sock.send(header)
        sock.send(filename_bits)

        data = f.read(4096)
        while data:
            print("sending... ")
            sock.send(data)
            data = f.read(4096)

finally:
    print("closing socket")
    sock.close()
