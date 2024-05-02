from dbcontroler import UserDBController, MessageDBController
import datetime
from abc import ABC, abstractmethod


class BaseChat(ABC):
    @abstractmethod
    def get_attr_names(self):
        """to be used in Repository classes;
        returns names of columns of object's coresponding table in the database"""
        pass

    @abstractmethod
    def get_attr_val(self):
        """to be used in Repository classes;
        returns values that should be stored in the database, representing object's attributes;
        if the attribute is container type(User), it will return int id;"""
        pass



class User(BaseChat):
    def __init__(self, id: int=-1, username: str="", password: str="", active=0):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def __str__(self):
        return f"User {self.id} - {self.username} - {self.password} - {self.active}"

    def get_attr_names(self):
        return tuple(("id", "username", "password", "active"))

    def get_attr_val(self):
        return tuple((self.id, self.username, self.password, self.active))


class Message(BaseChat):
    def __init__(self, id:int = -1, sender: User=None, recipient: User=None, content: str="", date: datetime=None):
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.date = date

    def get_attr_names(self):
        return tuple(("id", "sender", "recipient", "content", "date"))

    def get_attr_val(self):
        return tuple((self.id, self.sender.id, self.recipient.id, self.content, self.date))


class UserAdapter():
    """This class adds database functionality to User class -
     it calls database controller class to do the operations with database"""
    def __init__(self):
        self.db_controller = UserDBController()

    def create(self, user):
        result = self.db_controller.create(user)
        if result != -1:
            user.id = result
            return True
        return False

    def get_user(self, user, **kwargs) -> bool:
        result = self.db_controller.find(user, **kwargs)   # result is array of User objects
        if len(result) == 1:
            user.id = result[0][0]
            user.username = result[0][1]
            user.password = result[0][2]
            user.active = result[0][3]
            return True
        else:
            txt = "User not found" if len(result) == 0 else "User not unique"
            print(txt)
            return False

    def get_all_users(self):
        result = self.db_controller.find(User())
        users = []
        for user in result:
            users.append(User(user[0], user[1], user[2], user[3]))
        return users

    def set_active(self, user, sgn: bool) -> bool:
        user.active = 1 if sgn else 0
        if self.db_controller.update(user):
            return True
        else:
            return False


class MessageAdapter:
    """This class adds database functionality to Message class -
    it calls database controller class to do the operations with database"""
    def __init__(self):
        self.db_controller = MessageDBController()

    def saveMessage(self, msg):    # not refactored
        id = self.db_controller.create(msg)
        if id != -1:
            msg.id = id
            return True
        else:
            return False

    def get_conversation(self, user_1: User=None, user_2: User=None) -> dict:
        return self.db_controller.get_conversation(user_1.id, user_2.id)



