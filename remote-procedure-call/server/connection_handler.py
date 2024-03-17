import socket
from data_parser import DataParser

class ConnectionHandler:
    def __init__(self, connection: socket.socket, client_address) -> None:
        self.connection: socket.socket = connection
        self.client_address = client_address

    def handle_connection(self) -> None:
        try:
            received_data = self.receive_data()
            response = DataParser.parse(received_data)
            self.send_response(response)
        finally:
            self.connection.close()

    def receive_data(self) -> bytes:
        """クライアントからのバイナリデータを受け取る"""

        received_data = b""
        while True:
            data = self.connection.recv(32)
            if not data:
                break
            received_data += data
        return received_data
        
    def send_response(self, response: str) -> None:
        self.connection.sendall(response.encode())
