from controller import Controller

"""
Use cases testing:
1. signup - a) new credentials, b) credentials already exist  +
    c) load all users, d) load current user per ID +
2.login - a) existing user, b) wrong credentials (username or password) +
3. send message
4. receive message +
4. close session
5. load all users +
6. load messages with one friend +
"""

# SIGNUP
def signup(username="nemame") ->int:
    print("\n\n IN SIGNUP:")
    c = Controller()
    user_dict = c.signup(username, "1234")
    print(user_dict)
    print(c.response_ok)
    print(c.code)
    return user_dict['id']

def load_all_users():
    """loading friends list"""
    print("IN load_all_users():")
    c = Controller()
    users = c.load_users()
    print(users)

def load_user(id=None):
    """load current user"""
    print("IN load_user():")
    c = Controller()
    id = id if id else 6
    user = c.load_user(id)
    print(user)


# LOGIN
def login(username):
    print("\n\n IN LOGIN:")
    c = Controller()
    user = c.login(username, "1234")
    print("NEW LOGIN:", user)
    return user["id"]

def load_messages():
    c = Controller()
    messages = c.load_conversation(1, 2)
    for message in messages:
        print(messages[message])
    print(c.response_ok)
    print("Code: ", c.code)

def received_message():
    c = Controller()
    c.received_message(1, 2, "Hello again from test")
    load_messages()

def logout(username):
    print("\n\n IN LOGOUT:")
    id = login(username)
    c = Controller()
    print("NEW LOGOUT:", id)
    c.logout(id)
    load_user(id)


if __name__ == "__main__":
    signup("kuku")
    login("nikita")
    logout("Toad")
    load_all_users()
    load_user("Princes")

    load_messages()
    received_message()
