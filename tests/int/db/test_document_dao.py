import unittest
import sqlite3
import os
from src.ragtag.db.document_dao import DocumentDAO
from src.ragtag.db.db_connection import DBConnection

class TestDocumentDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = "test_database.db"

    def setUp(self):
        self.db_connection = DBConnection(self.db_path)
        
        self.connection = self.db_connection.create_connection()
        self.cursor = self.connection.cursor()
        
        sql_script_path = 'src/ragtag/db/schema/create_docs_table.sql'
        
        with open(sql_script_path, 'r') as sql_file:
            sql_script = sql_file.read()
        self.cursor.executescript(sql_script)
        self.connection.commit()

        self.document_dao = DocumentDAO(self.db_connection)

    def tearDown(self):
        self.connection.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_document_success(self):
        document_text = "This is a test document."
        document_id = self.document_dao.create_document(document_text)
        self.assertIsNotNone(document_id, "The document ID should not be None after successful creation.")
        self.cursor.execute("SELECT text FROM docs WHERE id=?", (document_id,))
        result = self.cursor.fetchone()
        self.assertEqual(document_text, result[0], "The document text in the database should match the inserted text.")

    def test_read_document_success(self):
        document_text = "This is a test document."
        document_id = self.document_dao.create_document(document_text)
        retrieved_document = self.document_dao.read_document(document_id)
        self.assertEqual(document_text, retrieved_document, "The retrieved document should match the inserted document.")

    def test_update_document_success(self):
        document_text = "This is a test document."
        document_id = self.document_dao.create_document(document_text)
        updated_document_text = "This is an updated test document."
        success = self.document_dao.update_document(document_id, updated_document_text)
        self.assertTrue(success, "The document should be successfully updated.")
        self.cursor.execute("SELECT text FROM docs WHERE id=?", (document_id,))
        result = self.cursor.fetchone()
        self.assertEqual(updated_document_text, result[0], "The document text in the database should match the updated text.")

    def test_delete_document_success(self):
        document_text = "This is a test document."
        document_id = self.document_dao.create_document(document_text)
        success = self.document_dao.delete_document(document_id)
        self.assertTrue(success, "The document should be successfully deleted.")
        self.cursor.execute("SELECT text FROM docs WHERE id=?", (document_id,))
        result = self.cursor.fetchone()
        self.assertIsNone(result, "The document should be deleted from the database.")

if __name__ == '__main__':
    unittest.main()
