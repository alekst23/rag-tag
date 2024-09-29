import sqlite3
from sqlite3 import Error

class DBConnection:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.new_connection()

    def new_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
        return conn

    def create_connection(self):
        if self.conn is None:
            self.conn = self.new_connection()
        return self.conn