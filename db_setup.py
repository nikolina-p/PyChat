import sqlite3
import os

db_name = os.path.join("Database", "pychat.db")

def create_database(name: str):
    con = sqlite3.connect(name)
    cur = con.cursor()

    cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, active INTEGER)")
    cur.execute("CREATE TABLE message(id INTEGER PRIMARY KEY AUTOINCREMENT, sender INTEGER, recipient INTEGER, content TEXT, date TEXT)")

    con.commit()
    con.close()


def check_database(name: str):
    con = sqlite3.connect(name)
    cur = con.cursor()

    res = cur.execute("SELECT name FROM sqlite_master")
    res.fetchone()
    print(res)

    con.close()


if __name__ == "__main__":
    create_database(db_name)
    check_database(db_name)
