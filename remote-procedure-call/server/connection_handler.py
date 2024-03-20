import socket
from data_parser import DataParser

import math

class ConnectionHandler:
    def __init__(self, connection: socket.socket, client_address) -> None:
        self.connection: socket.socket = connection
        self.client_address = client_address

    def handle_connection(self) -> None:
        try:
            received_data = self.receive_data()
            request_json = DataParser.parse(received_data)
            
            methods = {
                "floor" : "",
                "nroot" : "",
                "reverse" : "",
                "sort" : "",
                "validAnagram" : "",
            }

            self.send_response("")
        finally:
            self.connection.close()

    def receive_data(self) -> bytes:
        received_data = b""
        while True:
            data = self.connection.recv(32)
            if not data:
                break
            received_data += data
        return received_data
        
    def send_response(self, response: str) -> None:
        self.connection.sendall(response.encode())

    # 計算関数たち
    def floor(self, x: float) -> int:
        return math.floor(x)
    
    def nroot(self, n: int, x: int) -> float:
        return math.pow(x, 1/n)
    
    def reverse(self, s: str) -> str:
        return s[::-1]
    
    def valid_anagram(self, s1: str, s2: str) -> bool:
        s1 = ''.join(filter(str.isalpha, s1.lower()))
        s2 = ''.join(filter(str.isalpha, s2.lower()))

        count_s1 = {}
        count_s2 = {}

        for char in s1:
            count_s1[char] = count_s1.get(char, 0) + 1
        for char in s2:
            count_s2[char] = count_s2.get(char, 0) + 1

        return count_s1 == count_s2
    
    def sort(str_arr: list):
        return str_arr.sort()

