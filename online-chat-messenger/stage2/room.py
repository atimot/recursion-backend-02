from user import User

class Room:
    users: dict[str, User] = {}

    def __init__(self, name: str, owner: User, owner_token: str) -> None:
        self._name = name
        self._owner = owner
        self.add_user(owner, owner_token)

    def get_owner(self) -> User:
        return self.owner
    
    def get_name(self) -> str:
        return self._name
    
    def add_user(self, user: User, token: str) -> None:
        self.users[token] = user

    def get_user(self, token: str) -> User:
        return self.users.get(token)