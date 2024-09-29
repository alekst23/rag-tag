# src/db/tags_dao.py

import sqlite3
import numpy as np
from .db_connection import DBConnection
from .vector_index import VectorIndex

class TagsDAO:
    def __init__(self, db_connection: DBConnection, vector_index: VectorIndex):
        self.db_connection = db_connection
        self.vector_index = vector_index
        self.load_existing_embeddings()

    def add_tag(self, tag: str, embedding: list, faiss_id: int) -> int:
        # Convert list of floats to numpy array
        embedding_np = np.array(embedding, dtype=np.float32)
        # Serialize numpy array to bytes
        embedding_bytes = embedding_np.tobytes()

        #with self.db_connection.create_connection() as connection:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO tags (tag, embedding, faiss_id) VALUES (?, ?, ?)", (tag, embedding_bytes, faiss_id))
            connection.commit()
            
            return tag
        except sqlite3.IntegrityError:
            # If the tag exists, ensure its embedding is in the VectorIndex
            return tag
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")

    def get_tag(self, tag: str) -> tuple[int, list]:
        #with self.db_connection.create_connection() as connection:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT tag, embedding FROM tags WHERE tag = ?", (str(tag),))
            result = cursor.fetchone()
            if result:
                tag = result[0]
                embedding_np = np.frombuffer(result[1], dtype=np.float32)
                return tag, embedding_np
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")

    def load_existing_embeddings(self):
        #with self.db_connection.create_connection() as connection:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT tag, embedding FROM tags")
            results = cursor.fetchall()
            for row in results:
                tag = row[0]
                embedding_np = np.frombuffer(row[1], dtype=np.float32)
                self.vector_index.add_embedding(tag, embedding_np)
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")

    def delete_tag(self, tag: str) -> bool:
        #with self.db_connection.create_connection() as connection:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM tags WHERE tag = ?", (str(tag),))
            connection.commit()
            return True
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")
            
    def get_tag_by_faiss_id(self, faiss_id: int) -> str:
        #with self.db_connection.create_connection() as connection:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT tag FROM tags WHERE faiss_id = ?", (int(faiss_id),))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")
            
    def get_tags_by_faiss_ids(self, faiss_ids: list) -> list:
        """
        Retrieves tags from the database for a given list of faiss_ids.

        :param faiss_ids: List of faiss_ids to retrieve tags for.
        :return: List of tags corresponding to the given faiss_ids.
        """
        # with self.db_connection.create_connection() as connection:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        # Prepare a query string with the correct number of placeholders
        placeholders = ','.join('?' for _ in faiss_ids)
        query = f"SELECT tag FROM tags WHERE faiss_id IN ({placeholders})"
        cursor.execute(query, faiss_ids)
        # Fetch all matching rows
        rows = cursor.fetchall()
        # Extract tags from rows
        tags = [row[0] for row in rows]
        return tags