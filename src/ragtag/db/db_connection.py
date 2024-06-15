import sqlite3
from sqlite3 import Error

class DBConnection:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
        return conn
