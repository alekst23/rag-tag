import unittest
import sqlite3
import os
from src.db.db_connection import DBConnection
from src.backend.ragtag import RagTag

class TestRagTagIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = "test_database.db"
        cls.db_connection = DBConnection(cls.db_path)
        
        # Setup database schema
        cls.setupDatabaseSchema(cls.db_connection.create_connection())

        cls.ragtag = RagTag(cls.db_connection)

    @classmethod
    def setupDatabaseSchema(cls, connection):
        schema_files = [
            'src/db/schema/create_docs_table.sql',
            'src/db/schema/create_tags_table.sql',
            'src/db/schema/create_doc_tags_table.sql'
        ]
        cursor = connection.cursor()
        for script_path in schema_files:
            with open(script_path, 'r') as sql_file:
                sql_script = sql_file.read()
            cursor.executescript(sql_script)
        connection.commit()

    @classmethod
    def tearDownClass(self):
        self.cursor.execute("DROP TABLE docs")
        self.cursor.execute("DROP TABLE tags")
        self.cursor.execute("DROP TABLE doc_tags")
        self.connection.commit()

        self.cursor.close()
        self.connection.close()
        os.remove(self.db_path)

    def setUp(self):
        # Setup for individual tests if needed
        pass

    def tearDown(self):
        # Cleanup for individual tests if needed
        pass

    def test_add_single_document(self):
        document_text = "This is a test document."
        document_id = self.ragtag.add_document(document_text)
        self.assertIsNotNone(document_id, "Document ID should not be None")

        # Verify tags were generated and stored
        tags = self.ragtag.doc_tags_dao.get_doc_tags(document_id)
        self.assertTrue(len(tags) > 0, "Tags should be generated for the document")

    def test_add_multiple_documents(self):
        documents = [
            "First test document.",
            "Second test document."
        ]
        document_ids = self.ragtag.add_documents_bulk(documents)
        self.assertEqual(len(document_ids), 2, "Two documents should be added")

        for document_id in document_ids:
            tags = self.ragtag.doc_tags_dao.get_doc_tags(document_id)
            self.assertTrue(len(tags) > 0, "Tags should be generated for each document")

    def test_search_documents(self):
        documents = [
            "Python is a programming language with a simple syntax.",
            "To create a list in Python, use square brackets.",
            "Pancakes usually contain flour, eggs, and milk."
        ]
        document_ids = self.ragtag.add_documents_bulk(documents)

        # Search for documents containing the word "Python"
        search_results = self.ragtag.search_documents("Python")
        self.assertEqual(len(search_results), 2, "Two documents should be returned")

        # Search for documents containing the word "Pancakes"
        search_results = self.ragtag.search_documents("Pancakes")
        self.assertEqual(len(search_results), 1, "One document should be returned")

        

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.db_path)

if __name__ == '__main__':
    unittest.main()
