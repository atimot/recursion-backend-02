import socket
from data_parser import DataParser
from calculator import Calculator

class ConnectionHandler:
    def __init__(self, connection: socket.socket, client_address) -> None:
        self.connection: socket.socket = connection
        self.client_address = client_address

    def handle_connection(self) -> None:
        try:
            received_data: bytes = self.receive_data()
            request_json: dict = DataParser.parse(received_data)
            req_method: str = request_json.get("method")
            params: list = request_json.get("params")
            param_types: list = request_json.get("param_types")
            id: int = request_json.get("id")
            
            methods: dict[str, callable] = {
                "floor": Calculator.floor,
                "nroot": Calculator.nroot,
                "reverse": Calculator.reverse,
                "validAnagram": Calculator.valid_anagram,
                "sort": Calculator.sort,
            }

            param_counts: dict[str, int] = {
                "floor": 1,
                "nroot": 2,
                "reverse": 1,
                "validAnagram": 2,
                "sort": 1,
            }

            if methods.get(req_method) == None:
                # メソッド名エラー
                self.send_response("invalid method name.")

            if len(params) != param_counts.get(req_method):
                # 引数エラー
                self.send_response("invalid arguments.")

            try:
                result = methods[req_method](*params)
                self.send_response(str(result))
            except ValueError:
                # 引数の型エラー
                self.send_response("invalid param_types.")
            
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
