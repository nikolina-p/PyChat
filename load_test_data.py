import sqlite3
from model import User, Message
import datetime
import os

db_name = os.path.join("Database", "pychat.db")
test_data = os.path.join("Database", "shakespeare.txt")

def delete_all_users():
    query = "DELETE FROM user"
    try:
       conn = sqlite3.connect(db_name)
       cursor = conn.cursor()
       cursor.execute(query)
       conn.commit()
       conn.close()
    except sqlite3.DatabaseError as e:
        print("DB error: ", e)


def delete_all_messages():
    query = "DELETE FROM message"
    try:
       conn = sqlite3.connect(db_name)
       cursor = conn.cursor()
       cursor.execute(query)
       conn.commit()
       conn.close()
    except sqlite3.DatabaseError as e:
        print("DB error: ", e)


def fill_up_users():
    usernames = ["Mario", "Luigi", "Bowser", "Princes", "Toad"]
    password = "1234"
    for name in usernames:
        user = User()
        user.username = name
        user.password = "1234"
        insert_user(user)


def insert_user(user):
    query = f"INSERT INTO user (username, password) VALUES ('{user.username}', '{user.password}')"

    try:
       conn = sqlite3.connect(db_name)
       cursor = conn.cursor()
       cursor.execute(query)
       conn.commit()
       conn.close()
    except sqlite3.DatabaseError as e:
        print("DB error(41): ", e)


def print_users():
    query = "SELECT * FROM user"
    rows = ""
    try:
       conn = sqlite3.connect(db_name)
       cursor = conn.cursor()
       rows = cursor.execute(query)
       for row in rows:
           print(row)
       conn.commit()
       conn.close()
    except sqlite3.DatabaseError as e:
        print("DB error (54): ", e)


def fill_up_messages():
    lines = ""
    with open(test_data, 'r') as f:
        lines = f.read()
    messages_str = []
    for line in lines.split("\n"):
        messages_str.append(line)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user")
    ids = cursor.fetchall()

    delete = "DELETE FROM message"
    insert = f"INSERT INTO message (sender, recipient, content, date) VALUES (?, ?, ?, ?)"

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
    delete_all_users()
    delete_all_messages()
    fill_up_users()
    print_users()
    fill_up_messages()
    select_messages()