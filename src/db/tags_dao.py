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

        with self.db_connection.create_connection() as connection:
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
        with self.db_connection.create_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT tag, embedding FROM tags WHERE tag = ?", (tag,))
                result = cursor.fetchone()
                if result:
                    tag = result[0]
                    embedding_np = np.frombuffer(result[1], dtype=np.float32)
                    return tag, embedding_np
                else:
                    return None
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

    def load_existing_embeddings(self):
        with self.db_connection.create_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT tag, embedding FROM tags")
                results = cursor.fetchall()
                for row in results:
                    tag = row[0]
                    embedding_np = np.frombuffer(row[1], dtype=np.float32)
                    self.vector_index.add_embedding(tag, embedding_np)
            except Exception as e:
                print(f"An error occurred: {e}")

    def delete_tag(self, tag: str) -> bool:
        with self.db_connection.create_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM tags WHERE tag = ?", (tag,))
                connection.commit()
                return True
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
