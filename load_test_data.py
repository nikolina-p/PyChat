import sqlite3
from domain import User, Message
import datetime

db_name = "pychat.db"

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

def fill_up_users():
    usernames = ["Mario", "Luigi", "Bowser", "Princes", "Toad"]
    password = "1234"
    for name in usernames:
        user = User()
        user.username = name
        user.password = "1234"
        user.create()


def print_users():
    user = User()
    users = user.get_all_users()
    for user in users:
        print(user)


def fill_up_messages():
    lines = ""
    with open("shakespeare.txt", 'r') as f:
        lines = f.read()
    messages_str = []
    for line in lines.split("\n"):
        messages_str.append(line)
    print(messages_str)

    conn = sqlite3.connect(db_name)
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
    fill_up_users()
    print_users()
    fill_up_messages()
    select_messages()