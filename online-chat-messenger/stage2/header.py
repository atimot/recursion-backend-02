class Header:
    ROOM_CREATE: int = 1
    ROOM_JOIN: int = 2

    STATE_REQUESTED: int = 0
    STATE_CONFORMANCE: int = 1
    STATE_COMPLETE: int = 2

    room_name_size: int
    operation: int
    state: int
    operation_payload_size: int

    def __init__(self, data: bytes) -> None:
        self.room_name_size = int.from_bytes(data[:1], "big")
        self.operation = int.from_bytes(data[1:2], "big")
        self.state = int.from_bytes(data[2:3], "big")
        self.operation_payload_size = int.from_bytes(data[3:], "big")

    def validate(self) -> bool:
        if not self.operation in (Header.ROOM_CREATE, Header.ROOM_JOIN):
            return False
        
        if not self.state == Header.STATE_REQUESTED:
            return False
        
        return True
    
    @staticmethod
    def create_header_from_byte():
        return Header()
    
    @staticmethod
    def create_header_from_data():
        return Header()
    
    @staticmethod
    def protocol_header(room_name_size: int, operation: int, state: int, operation_payload_size: int) -> bytes:
        return (
            room_name_size.to_bytes(1, "big")
            + operation.to_bytes(1, "big")
            + state.to_bytes(1, "big")
            + operation_payload_size.to_bytes(29, "big")
        )