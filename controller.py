import datetime

from model import User, Message, UserAdapter, MessageAdapter


class Controller:
    """
    This class holds all use-cases of the app:
     - it creates domain objects,
     - calls UserAdapter and MessageAdapter to execute the requested actions or get data from the database,
     - prepares the responses (dict - ready for JSON.dump) and returns them to app.py.
    """
    def __init__(self):
        self.response_ok = True
        self.code = 0
        self.user_adapter = UserAdapter()
        self.message_adapter = MessageAdapter()

    def signup(self, username, password):
        user = User(username=username, password=password)
        user_dict = {}

        sgn = self.user_adapter.get_user(user, username=username, password=password)

        if sgn or user.id != -1:
            self.response_ok = False
            self.code = "User already exists"
            return user_dict

        sgn = self.user_adapter.create(user)

        if sgn:
            self.response_ok = True
            self.code = "ok"
            user_dict = {"id": user.id, "username": user.username, "active": user.active}
        else:
            self.response_ok = False
            self.code = "Error while saving user"

        return user_dict


    def login(self, username, password):
        user = User(username=username, password=password)
        user_dict = {}

        sgn = self.user_adapter.get_user(user, username=username, password=password)

        if not sgn:
            self.response_ok = False
            self.code = "User does not exist"
            return user_dict

        if user.active == 1:
            self.response_ok = False
            self.code = "User already logged in"
            return user_dict

        sgn = self.user_adapter.set_active(user, True)

        if not sgn:
            self.response_ok = False
            self.code = "Error while activating user"
            return user_dict

        self.response_ok = True
        self.code = "ok"

        user_dict = {"id": user.id, "username": user.username, "active": user.active}

        return user_dict

    def load_users(self):
        users = self.user_adapter.get_all_users()

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

        if self.user_adapter.get_user(user, id=user.id):
            self.response_ok = True
            self.code = "User found"
            user_dict = {"id": user.id, "username": user.username, "active": user.active}
        else:
            self.response_ok = False
            self.code = "User does not exist"

        return user_dict

    def logout(self, id) -> bool:
        user = User(id)

        sgn = self.user_adapter.get_user(user, id=id)

        if not sgn:
            self.response_ok = False
            self.code = "User does not exist"
            return False

        if self.user_adapter.set_active(user, False):
            self.response_ok = "ok"
            self.code = "User deactivated"
            return True
        else:
            self.response_ok = False
            self.code = "Error while deactivation user"
            return False

    def received_message(self, from_id, to_id, message) -> list:
        from_user = User()
        sgn1 = self.user_adapter.get_user(from_user, id=from_id)

        to_user = User()
        sgn2 = self.user_adapter.get_user(to_user, id=to_id)

        if sgn1 and sgn2:
            message = Message(sender=from_user, recipient=to_user, content=message, date=datetime.datetime.now())
            if self.message_adapter.saveMessage(message):
                self.response_ok = True
                self.code = "New message saved"
            else:
                self.response_ok = False
                self.code = "Problem saving message"
            return self.response_ok
        else:
            self.response_ok = False
            self.code = "Users not valid."
            return self.response_ok

    def load_conversation(self, id_1, id_2) -> dict:
        user_1 = User()
        user_2 = User()
        msg_dict = {}
        # check if users exist
        if self.user_adapter.get_user(user_1, id=id_1) and self.user_adapter.get_user(user_2, id=id_2):
            msg = Message()
            response = self.message_adapter.get_conversation(user_1, user_2)

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
        else:
            self.response_ok = False
            self.code = "User not found"

        return msg_dict


if __name__ == "__main__":
    controller = DomainController()
