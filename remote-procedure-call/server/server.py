import socket
import os 
from connection_handler import ConnectionHandler

class Server:
    def __init__(self, address: str) -> None:
        self.address = address
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.prepare_socket()
    
    def prepare_socket(self) -> None:
        if os.path.exists(self.address):
            os.unlink(self.address)
        self.sock.bind(self.address)
        self.sock.listen(1)
        print(f"starting up on {self.address}")

    def accept_connections(self, handler: type[ConnectionHandler]) -> None:
        connection, client_address = self.sock.accept()
        print(f"connection from {client_address}")
        handler(connection, client_address).handle_connection()

if __name__ == "__main__":
    server_address = "/tmp/socket_file"
    server = Server(server_address)
    while True:
        server.accept_connections(ConnectionHandler)
