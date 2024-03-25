from hashlib import sha256

from domain import User, Message


class DomainController:
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

    def hash_id(self, id):
        return sha256(str(id).encode()).hexdigest()

    def unhash_secret(self, secret):
        hash_bytes = bytes.fromhex(secret)
        original_bytes = sha256(hash_bytes).digest()
        user_id = int.from_bytes(original_bytes, byteorder='big')
        return user_id


if __name__ == "__main__":
    controller = DomainController()
    x = controller.hash_id(5)
    print(x)
    y = controller.unhash_secret(x)
    print(y)