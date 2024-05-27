import unittest
import sqlite3
import os
import numpy as np
from numpy.testing import assert_array_equal
from src.db.tags_dao import TagsDAO
from src.db.db_connection import DBConnection
from src.db.vector_index import VectorIndex
from src.backend.llm import EMBEDDING_SIZE


class TestTagsDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = "test_database.db"
        cls.schema_path = 'src/db/schema/create_tags_table.sql'

    def setUp(self):
        # Set up an in-memory SQLite database and initialize TagsDAO
        self.db_connection = DBConnection(self.db_path)
        
        self.connection = self.db_connection.create_connection()
        self.cursor = self.connection.cursor()
        
        # Load and execute the schema from create_tags_table.sql
        with open(self.schema_path, 'r') as schema_file:
            schema_sql = schema_file.read()
        self.cursor.executescript(schema_sql)
        self.connection.commit()

        # Set up a vector store
        self.vector_index = VectorIndex(dimension=EMBEDDING_SIZE)   

        self.tags_dao = TagsDAO(self.db_connection, self.vector_index)

    def tearDown(self):
        self.connection.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_add_tag(self):
        tag = "test_tag"
        embedding = np.random.rand(128).astype(np.float32)
        faiss_id = 1
        self.tags_dao.add_tag(tag, embedding, faiss_id)
        
        self.cursor.execute("SELECT tag, embedding, faiss_id FROM tags WHERE tag=?", (tag,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(tag, result[0])
        self.assertTrue(isinstance(result[1],bytes))
        self.assertEqual(faiss_id, result[2])

    def test_get_tag(self):
        tag = "test_tag"
        embedding = np.random.rand(128).astype(np.float32)
        faiss_id = 1
        self.tags_dao.add_tag(tag, embedding, faiss_id)
        
        retrieved_tag  = self.tags_dao.get_tag(tag)
        self.assertEqual(tag, retrieved_tag[0])
        assert_array_equal(embedding, retrieved_tag[1])

    def test_delete_tag(self):
        tag = "test_tag"
        embedding = np.random.rand(128).astype(np.float32)
        self.tags_dao.add_tag(tag, embedding, 1)
        self.tags_dao.delete_tag(tag)
        
        self.cursor.execute("SELECT tag FROM tags WHERE tag=?", (tag,))
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_search_tags(self):
        # This test would require more setup to properly test FAISS functionality
        pass

if __name__ == '__main__':
    unittest.main()
