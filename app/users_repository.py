from attrs import define


@define
class User:
    email: str
    full_name: str
    password: str
    id: int = 0


class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = []

    def signup(self, email, full_name, password):
        user = User(email, full_name, password, self.get_next_id())
        self.users.append(user)
        return user
    
    def get_next_id(self):
        return len(self.users)
    
    def get_user_by_email(self, email):
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    def get_user_by_id(self, id):
        for user in self.users:
            if user.id == id:
                return user
