import json

class DataParser:
    @staticmethod
    def parse(data: bytes) -> str:
        data_str = data.decode("utf-8")
        json_data = json.loads(data_str)

        method: str|None = json_data.get("method")
        params: list|None = json_data.get("params")
        param_types: list|None = json_data.get("param_types")
        id: int|None = json_data.get("id")

        response = f"response OK. {method}, {params}, {param_types}, {id}"
        return response
