import sqlite3
import os
import copy

class Repository:
    def __init__(self):
        self.name = os.path.join("Database", "pychat.db")
        self.connection = None
        self.cursor = None

    def db_open(self):
        try:
            self.connection = sqlite3.connect(self.name)
            print("Connected to database")
        except sqlite3.Error as e:
            print(f"Error while connecting to {self.name}: ", e.get_message())

    def close(self):
        try:
            if self.connection:
                self.connection.close()
                print("Connection closed.")
            else:
                print("No connection to database.")
        except sqlite3.Error as e:
            print("Error closing connection:", e)

    def create(self, object):
        table_name = object.__class__.__name__.lower()
        fields = ", ".join(tuple(object.__dict__.keys())[1:])
        placeholders = ", ".join(["?" for _ in object.__dict__.values()][1:])
        values = object.get_attr_val()[1:]
        result = -1

        self.db_open()

        try:
            query = f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})"

            cursor = self.connection.cursor()
            cursor.execute(query, values)
            result = cursor.lastrowid         # set the ID of the new user
            self.connection.commit()

            print(f"{table_name.capitalize()} created successfully")

        except sqlite3.Error as e:
            print(f"Error creating {table_name}: {e}")

        self.close()
        return result

    def update(self, object) -> bool:
        """update the row with same id as object's id"""
        table_name = object.__class__.__name__.lower()
        fields = ", ".join([f"{key} = ?" for key in object.__dict__.keys()])
        placeholders = ", ".join(["?" for _ in object.__dict__])
        values = tuple(object.__dict__.values())
        sgn = False

        self.db_open()

        try:
            query = f"UPDATE {table_name} SET {fields} WHERE id={object.id}"

            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()

            if cursor.rowcount > 0:
                print(f"{table_name.capitalize()} updated successfully")
                sgn = True
            else:
                print(f"No such {table_name.capitalize()} in DB")
                sgn = False

        except sqlite3.Error as e:
            print(f"Error updating {table_name}: {e}")
            sgn = False

        self.close()
        return sgn

    def find(self, object, **kwargs) -> bool:
        """returns list of objects that maches keyword arguments"""
        table_name = object.__class__.__name__.lower()
        query = f"SELECT * FROM {table_name}"

        if len(kwargs) > 0:
            query += " WHERE "
            for key, value in kwargs.items():
                query += f"{key} = '{value}' AND "
            query = query[:-5]

        self.db_open()

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error while finding {table_name}: {e}")

        self.close()
        return rows

    def delete(self, object, **kwargs) -> bool:
        """
        deletes the rows that matche keyword arguments
        if no keyword arguments are passed, it will delete all rows in the table
        """
        table_name = object.__class__.__name__.lower()
        query = f"DELETE FROM {table_name}"
        result = []

        if len(kwargs) > 0:
            query += " WHERE "
            for key, value in kwargs.items():
                query += f"{key} = '{value}' AND "
            query = query[:-5]

        self.db_open()

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()

            if cursor.rowcount > 0:
                print(f"{table_name} deleted successfully.")
            else:
                print(f"No such {table_name} found.")
        except sqlite3.Error as e:
            print(f"Error while deleting from {table_name}")

        self.close()


class UserRepository(Repository):
    pass


class MessageRepository(Repository):

    def get_conversation(self, userid_1, userid_2):
        query = (f"SELECT * FROM message WHERE (sender = ? and recipient = ?) "
                 f"or (sender = ? and recipient = ?) order by id ASC ")
        values = (userid_1, userid_2, userid_2, userid_1)

        self.db_open()

        try:
            connection = self.connection.cursor()
            result = connection.execute(query, values)
            result = result.fetchall()

        except sqlite3.Error as e:
            print(f"Error while getting messages from user ID {userid_1}")
            result = -1

        self.close()
        return result
