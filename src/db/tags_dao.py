# src/db/tags_dao.py

import sqlite3
import numpy as np
from .db_connection import DBConnection
from .vector_index import VectorIndex

class TagsDAO:
    def __init__(self, db_connection: DBConnection, vector_dimension=128):
        self.db_connection = db_connection
        self.vector_index = VectorIndex(dimension=vector_dimension)
        self.load_existing_embeddings()

    def add_tag(self, tag: str, embedding: bytes) -> None:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("INSERT INTO tags (tag, embedding) VALUES (?, ?)", (tag, embedding))
            connection.commit()
            embedding_np = np.frombuffer(embedding, dtype=np.float32)
            self.vector_index.add_embedding(embedding_np)
        except sqlite3.IntegrityError:
            print(f"Tag '{tag}' already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()

    def get_tag(self, tag: str) -> tuple:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("SELECT tag, embedding FROM tags WHERE tag=?", (tag,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            connection.close()

    def delete_tag(self, tag: str) -> None:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute("DELETE FROM tags WHERE tag=?", (tag,))
            connection.commit()
            self.vector_index.remove_embedding(tag)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()

    def search_tags(self, search_embedding: bytes, top_n: int) -> list:
        query_embedding = np.frombuffer(search_embedding, dtype=np.float32)
        return self.vector_index.search(query_embedding, top_n)

    def load_existing_embeddings(self):
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT embedding FROM tags")
            embeddings = [np.frombuffer(row[0], dtype=np.float32) for row in cursor.fetchall()]
            if embeddings:
                self.vector_index.add_embeddings(embeddings)
        except Exception as e:
            print(f"An error occurred while loading existing embeddings: {e}")
        finally:
            connection.close()
