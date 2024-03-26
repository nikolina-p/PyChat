import sqlite3

db_name = "pychat.db"

def create_database(name: str):
    con = sqlite3.connect(name)
    cur = con.cursor()

    cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, active INTEGER)")
    cur.execute("CREATE TABLE message(id INTEGER PRIMARY KEY, sender_id INTEGER, recipient_id INTEGER, message TEXT, date TEXT)")

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
