import unittest
import sqlite3
import os
from src.db.doc_tags_dao import DocTagsDAO
from src.db.db_connection import DBConnection

class TestDocTagsDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = "test_database.db"
        cls.db_connection = DBConnection(cls.db_path)

    def setUp(self):
        self.connection = self.db_connection.create_connection()
        self.cursor = self.connection.cursor()

        # Create tables for testing
        self.cursor.execute("CREATE TABLE IF NOT EXISTS doc_tags (doc_id INTEGER, tag_id INTEGER, tag TEXT)")
        self.connection.commit()

        self.doc_tags_dao = DocTagsDAO(self.db_connection)

    def tearDown(self):
        self.cursor.execute("DROP TABLE doc_tags")
        self.connection.commit()

        self.cursor.close()
        self.connection.close()
        os.remove(self.db_path)

    def test_add_tags_to_doc(self):
        doc_id = 1
        tag_ids = [101, 102]
        self.doc_tags_dao.add_tags_to_doc(doc_id, tag_ids)
        self.cursor.execute("SELECT tag_id FROM doc_tags WHERE doc_id=?", (doc_id,))
        tags_in_db = [row[0] for row in self.cursor.fetchall()]
        self.assertListEqual(tag_ids, tags_in_db)

    def test_get_doc_tags(self):
        doc_id = 2
        tags = ['python', 'unittest']
        for tag in tags:
            self.cursor.execute("INSERT INTO doc_tags (doc_id, tag) VALUES (?, ?)", (doc_id, tag))
        self.connection.commit()

        retrieved_tags = self.doc_tags_dao.get_doc_tags(doc_id)
        self.assertListEqual(tags, retrieved_tags)

    def test_get_tag_docs(self):
        tag = 'unittest'
        doc_ids = [1, 2]
        for doc_id in doc_ids:
            self.cursor.execute("INSERT INTO doc_tags (doc_id, tag) VALUES (?, ?)", (doc_id, tag))
        self.connection.commit()

        retrieved_doc_ids = self.doc_tags_dao.get_tag_docs(tag)
        self.assertListEqual(doc_ids, retrieved_doc_ids)

    def test_remove_doc_tags(self):
        doc_id = 3
        tags = ['cleanup', 'test']
        for tag in tags:
            self.cursor.execute("INSERT INTO doc_tags (doc_id, tag) VALUES (?, ?)", (doc_id, tag))
        self.connection.commit()

        self.doc_tags_dao.remove_doc_tags(doc_id)
        self.cursor.execute("SELECT * FROM doc_tags WHERE doc_id=?", (doc_id,))
        self.assertFalse(self.cursor.fetchall())

if __name__ == '__main__':
    unittest.main()
