from model import User, Message
from controller import Controller
import sqlite3
from repository import Repository
import os
import datetime

db_name = "Database/pychat.db"
repository = Repository()

# DATA BASE TESTS
def add_user():
    user = User(username="Maria", password="1234")
    repository.create(user)
    print(user.id)

def update_user():
    user = User(id=12, username="Tina", password="1234")
    repository.update(user)
    print(user.id, user.username, user.password)

def find_user():
    user = User()
    result = repository.find(user, username="Tina")
    print(result)

def find_all_users():
    user = User()
    result = repository.find(user)
    print(result)

def delete_user():
    user = User()
    repository.delete(user, id=99)
    find_all_users()

def find_all_messages():
    msg = Message()
    result = repository.find(msg)
    for m in result:
        print(m.id, m.sender, m.recipient, m.content, m.date)

def unactivate_users():
    """go strait to database"""
    query = "UPDATE user SET active = 0"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

def fix_message_primary_key():
    drop = "DROP TABLE IF EXISTS message"

    create = "CREATE TABLE message(id INTEGER PRIMARY KEY, sender_id INTEGER, recipient_id INTEGER, message TEXT, date TEXT)"

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(drop)
    cursor.execute(create)
    conn.commit()
    conn.close()

def select_messages():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    select = "SELECT * FROM message"

    cursor.execute(select)
    msgs = cursor.fetchall()

    conn.commit()
    conn.close()

    for item in msgs:
        print(item)


if __name__ == "__main__":
    print("REPOSITORY TESTING")
    #add_user()
    #update_user()
    #find_user()
    #find_all_users()
    #find_all_messages()
    #delete_user()

    #select_messages()
    #fix_message_primary_key()
    #unactivate_users()
