import socket
import os
from pathlib import Path

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ""
server_port = 9001

dpath = "temp"
if not os.path.exists(dpath):
    os.makedirs(dpath)

print(f"starting up on {server_address} port {server_port}")

sock.bind((server_address, server_port))
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        print(f"connection from {client_address}")
        header = connection.recv(8)

        filename_length = int.from_bytes(header[:1], "big")
        json_length = int.from_bytes(header[1:3], "big")
        data_length = int.from_bytes(header[4:8], "big")
        stream_rate = 4096

        print(f"received header from client. byte length: title length {filename_length}, JSON length {json_length}, data length {data_length}")

        filename = connection.recv(filename_length).decode("utf-8")

        print(f"filename: {filename}")

        if json_length != 0:
            raise Exception("JSON data is not currently supported.")
        if data_length == 0:
            raise Exception("no data to read from client.")
        
        with open(os.path.join(dpath, filename), "wb+") as f:
            while data_length > 0:
                data = connection.recv(data_length if data_length <= stream_rate else stream_rate)
                f.write(data)
                print(f"recived {len(data)} bytes")
                data_length -= len(data)
                print(data_length)

            print("finished downloading the file from client.")

    except Exception as e:
        print(f"error: {str(e)}")
    finally:
        print("closing current connection")
        connection.close()