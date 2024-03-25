import sqlite3


def create_database(name: str):
    con = sqlite3.connect(name)
    cur = con.cursor()

    cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, active INTEGER)")
    cur.execute("CREATE TABLE message(sender_id INTEGER PRIMARY KEY, recipient_id INTEGER, message TEXT, date TEXT)")

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
    # create_database("pychat.db")
    check_database("pychat.db")
