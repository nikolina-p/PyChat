import datetime

from model import User, Message


class Controller:
    """
    This class holds the application logic and responds to user's actions/requests.
    It creates domain objects and manipulates them.
    """
    def __init__(self):
        self.response_ok = True
        self.code = 0

    def signup(self, username, password):
        user = User(username=username, password=password)

        if user.signup():
            self.response_ok = True
            self.code = "ok"
        else:
            self.response_ok = False
            if user.id != -1:
                self.code = "user_exists"
            else:
                self.code = "unknown_error"

        user_dict = {"id": user.id, "username": user.username, "active": user.active}

        return user_dict


    def login(self, username, password):
        user = User(username=username, password=password)

        if user.login():
            self.response_ok = True
            self.code = "ok"
        else:
            self.response_ok = False
            self.code = "User is already loged in" if user.active == 1 else "Wrong username or password"

        user_dict = {"id": user.id, "username": user.username, "active": user.active}

        return user_dict

    def load_users(self):
        user = User()
        users = user.get_all_users()

        users_dict = dict()
        for user in users:
            users_dict[user.id] = {
                "id": user.id,
                "username": user.username,
                "active": user.active
            }
        return users_dict

    def load_user(self, id):
        user = User(id)
        user_dict = {}

        if user.get_user(id=user.id):
            self.response_ok = True
            self.code = "User found"
            user_dict = {"id": user.id, "username": user.username, "active": user.active}
        else:
            self.response_ok = False
            self.code = "User does not exist"

        return user_dict

    def deactivate_user(self, id) -> bool:
        user = User(id)
        if user.set_active(False):
            self.response_ok = "ok"
            self.code = "User deactivated"
            return True
        else:
            self.response_ok = False
            self.code = "Error when deactivating user"
        return False

    def received_message(self, from_id, to_id, message) -> list:
        from_user = User()
        from_user.get_user(id=from_id)

        to_user = User()
        to_user.get_user(id=to_id)

        message = Message(from_user, to_user, message, datetime.datetime.now())
        if message.saveMessage():
            self.response_ok = True
            self.code = "New message saved"
        else:
            self.response_ok = False
            self.code = "Problem saving message"
        return self.response_ok

    def load_conversation(self, id_1, id_2) -> dict:
        user_1 = User()
        user_2 = User()
        # check if they exist
        if user_1.get_user(id=id_1) and user_2.get_user(id=id_2):
            msg = Message()
            response = msg.get_conversation(user_1, user_2)

            msg_dict = {}
            if response != -1:
                # prepare the data for sending via websocket
                for message in response:
                    msg_dict[message[0]] = list(message)
                self.response_ok = True
                self.code = "Conversation loaded"
            else:
                # returned -1, DB problem
                self.response_ok = False
                self.code = "Problem loading messages from DB"

            return msg_dict


if __name__ == "__main__":
    controller = DomainController()
