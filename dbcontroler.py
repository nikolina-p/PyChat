import sqlite3

class dbcontroller:
    def __init__(self):
        self.name = "pychat.db"
        self.connection = None
        self.cursor = None

    def db_open(self):
        try:
            self.connection = sqlite3.connect(self.name)
            print("Connected to database")
        except sqlite3.Error as e:
            print(f"Error while connecting to {self.name}: ", e.get_message())

    # queries -> list of tuples (query string, values)
    def execute(self, queries):
        try:
            self.cursor = self.connection.cursor()
            for query, val in queries:
                if val:
                    self.cursor.execute(query, val)
                else:
                    self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error while executing {query} : ", e)
            return False

    def close(self):
        try:
            if self.connection:
                self.connection.close()
                print("Connection closed.")
            else:
                print("No connection to database.")
        except sqlite3.Error as e:
            print("Error closing connection:", e)

    def delete_all(self, table):
        query = f"DELETE FROM {table}"

        self.db_open()
        result = self.execute([(query, None)])
        self.close()
        return result


class UserDBController(dbcontroller):

    def create(self, username, pwd, active):
        query = f"INSERT INTO user (username, password, active) VALUES (?, ?, ?)"
        values = (username, pwd, active)

        self.db_open()

        if self.execute([(query, values)]):
            result = self.cursor.lastrowid
        else:
            result = -1
        self.close()
        return result

    def get_user(self, **kvargs):
        query = "SELECT * FROM user WHERE "
        for key, value in kvargs.items():
            query += f"{key} = '{value}' AND "
        query = query[:-5]

        self.db_open()
        self.execute([(query, None)])
        result = self.cursor.fetchall()
        self.close()
        return result

    def update(self, userid, **fields) -> bool:
        query = f"UPDATE user SET "
        for key, val in fields.items():
            query += f"{key} = '{val}', "
        query = query[:-2] + f" WHERE id={userid}"

        self.db_open()
        sgn = self.execute([(query, None)])
        self.close()
        return sgn

    def delete(self, **kvargs):
        query = f"DELETE FROM user WHERE "
        for key, value in kvargs.items():
            query += f"{key} = '{value}' AND "
        query = query[:-5]
        self.db_open()
        sgn = self.execute([(query, None)])
        self.close()
        return sgn


    def get_all_users(self):
        query = f"SELECT * FROM user"

        self.db_open()
        result = []
        if self.execute([(query, None)]):
            result = self.cursor.fetchall()
        self.close()

        return result


class MessageDBController(dbcontroller):

    def create(self, from_id, to_id, message, datetime):
        create = f"INSERT INTO message (sender_id, recipient_id, message, date) VALUES (?, ?, ?, ?)"

        values = (from_id, to_id, message, datetime)

        self.db_open()

        if self.execute([(create, values)]):
            result = self.cursor.lastrowid
        else:
            result = -1
        self.close()
        return result

    def get_conversation(self, user_1, user_2):
        query = (f"SELECT * FROM message WHERE (sender_id = ? and recipient_id = ?) "
                 f"or (sender_id = ? and recipient_id = ?) order by id ASC ")
        values = (user_1, user_2, user_2, user_1)

        self.db_open()
        if self.execute([(query, values)]):
            result = self.cursor.fetchall()
        else:
            result = -1
        self.close()
        return result
