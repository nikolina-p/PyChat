from domain import User, Message
from domaincontroller import DomainController
import sqlite3
from dbcontroler import UserDBController
import os
import datetime

def add_user():
    user = User(username="test2", password="1234")
    user.create()


def fill_up_users():
    usernames = ["Mario", "Luigi", "Bowser", "Princes", "Toad"]
    password = "1234"
    for name in usernames:
        user = User()
        user.username = name
        user.password = "1234"
        user.create()

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
    user = User(username="test", password="1234")
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

def empty_message_table():
    m = Message()
    result = m.delete_all()
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

    delete = "DELETE FROM message"
    insert = f"INSERT INTO message (sender_id, recipient_id, message, date) VALUES (?, ?, ?, ?)"

    cursor.execute(delete)

    i = 0
    for x in range(5): # make 5 messages for each
        for sender in ids:
            for receiver in ids:
                if sender != receiver:
                    values = (sender[0], receiver[0], messages_str[i], str(datetime.datetime.now()))
                    cursor.execute(insert, values)
                    i = (i + 1) if i < len(messages_str) - 1 else 0

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

def get_conversations():
    """gets the list of messages exchanged between two users"""
    m = Message()
    conv = m.get_conversation(User(id=13), User(id=12))
    for c in conv:
        print(c)

def sign_up_domain():
    dc = DomainController()
    ret = dc.signup("niko", "1234")
    print(ret)




if __name__ == "__main__":
    print("Hello World")
    #signup()
    #empty_user_table()
    #fix_message_primary_key()
    #delete_username()
    #update()
    #fill_up_users()
    #print_users()
    #query_db()
    #unactivate_users()
    fill_up_messages()
    select_messages()
    #empty_message_table()
    #get_conversations()

    #sign_up_domain()



