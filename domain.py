from dbcontroler import UserController
import datetime


class User:
    def __init__(self, id: int=-1, username: str="", password: str="", active=0):
        self.id = id
        self.username = username
        self.password = password
        self.active = active
        self.db_controller = UserController()

    def create(self):
        result = self.db_controller.create(self.username, self.password, self.active)
        if result != -1:
            self.id = result
            return True
        return False


    def delete(self):
        self.db_controller.delete_user(self)


    def get_user(self, **kvargs):
        result = self.db_controller.get_user(**kvargs)
        if len(result) == 1:
            self.id = result[0][0]
            self.username = result[0][1]
            self.password = result[0][2]
            self.active = result[0][3]
            return True
        else:
            return False

    def get_all_users(self):
        result = self.db_controller.get_all_users()
        users = []
        for user in result:
            users.append(User(user[0], user[1], user[2], user[3]))
        return users


    def signup(self):
        sgn = self.get_user(username=self.username)
        if sgn:
            return False
        self.active = 1
        return self.create()

    def login(self):
        sgn = self.get_user(username=self.username, password=self.password)
        if sgn:
            if self.active == 1:
                return False
            return self.set_active(True)
        return False

    def set_active(self, sgn: bool) -> bool:
        active = 1 if sgn else 0
        result = self.db_controller.update(self.id, active=active)
        return result


    def delete_all(self):
        result = self.db_controller.delete_all("user")
        return result


    def __str__(self):
        return f"{self.id}, {self.username}, {self.password}, {self.active}"


class Message:
    def __init__(self, sender: User, recipient: User, content: str, date: datetime):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.date = date
