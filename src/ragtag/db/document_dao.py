# src/db/document_dao.py

from .db_connection import DBConnection

class DocumentDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_document(self, document_text):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("INSERT INTO docs (text) VALUES (?)", (document_text,))
            document_id = cursor.lastrowid
            connection.commit()
            return document_id
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def read_document(self, document_id):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("SELECT text FROM docs WHERE id=?", (document_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def update_document(self, document_id, new_document_text):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("UPDATE docs SET text=? WHERE id=?", (new_document_text, document_id))
            connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def delete_document(self, document_id):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("DELETE FROM docs WHERE id=?", (document_id,))
            connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
