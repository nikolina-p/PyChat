from domain import User, Message
import sqlite3
from dbcontroler import UserController


def add_user():
    user = User("test", "1234")
    user.new()
    print(user)

def select():
    conn = sqlite3.connect('pychat.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    res = cursor.fetchall()
    conn.close()
    print("Result ",res)

def is_registered():
    user = User("test", "1234")
    print(user.is_registered())

def signup():
    user = User("new3", "1234")
    print("Signup: ", user.signup())

def print_users():
    user = User()
    users = user.get_all_users()
    for user in users:
        print(user)

def empty_user_table():
    user = User()
    result = user.delete_all()
    print(result)

def query_db():
    dbcont = UserController()
    result = dbcont.get_all_users()
    print(result)

def unactivate_users():
    user = User()
    users = user.get_all_users()
    for user in users:
        user.set_active(False)

    users = user.get_all_users()
    for user in users:
        print(user)

def delete_username():
    dbc = UserController()
    dbc.delete(username="bowser")

def update():
    dbc = UserController()
    dbc.update(12, username="bowser", password="1111")


if __name__ == "__main__":
    print("Hello World")
    #signup()
    #empty_user_table()
    #delete_username()
    #update()
    print_users()
    #query_db()
    unactivate_users()
