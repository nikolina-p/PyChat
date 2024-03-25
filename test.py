from domain import User, Message
import sqlite3
from dbcontroler import UserController
import os
import datetime


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

def fill_up_messages():
    lines = ""
    with open("shakespeare.txt", 'r') as f:
        lines = f.read()
    messages_str = []
    for line in lines.split("\n"):
        messages_str.append(line)
    print(messages_str)

    conn = sqlite3.connect('pychat.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user")
    ids = cursor.fetchall()

    insert = f"INSERT INTO message (sender_id, recipient_id, message, date) VALUES (?, ?, ?, ?)"

    recipient = -1
    for id in ids:
        for i in range(len(messages_str)//2):
            values = (id[0], ids[recipient][0], messages_str[i], str(datetime.datetime.now()))
            cursor.execute(insert, values)
        for i in range(len(messages_str)//2, len(messages_str)):
            values = (ids[recipient][0], id[0], messages_str[i], str(datetime.datetime.now()))
            cursor.execute(insert, values)

    conn.commit()
    conn.close()


def fix_message_primary_key():
    drop = "DROP TABLE IF EXISTS message"

    create = "CREATE TABLE message(id INTEGER PRIMARY KEY, sender_id INTEGER, recipient_id INTEGER, message TEXT, date TEXT)"

    conn = sqlite3.connect('pychat.db')
    cursor = conn.cursor()

    cursor.execute(drop)
    cursor.execute(create)
    conn.commit()
    conn.close()

def select_messages():
    conn = sqlite3.connect('pychat.db')
    cursor = conn.cursor()

    select = "SELECT * FROM message"

    cursor.execute(select)
    msgs = cursor.fetchall()

    conn.commit()
    conn.close()

    for item in msgs:
        print(item)


if __name__ == "__main__":
    print("Hello World")
    #signup()
    #empty_user_table()
    #fix_message_primary_key()
    #delete_username()
    #update()
    #print_users()
    #query_db()
    #unactivate_users()
    #fill_up_messages()
    #select_messages()

    d1 = datetime.datetime.now()
    d2 = datetime.datetime.now() + datetime.timedelta(hours=2)
    d3 = datetime.datetime.now() + datetime.timedelta(5)


    print(datetime.datetime.now() + datetime.timedelta(hours=3))

