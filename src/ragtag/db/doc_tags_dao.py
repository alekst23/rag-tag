# src/db/doc_tags_dao.py

from .db_connection import DBConnection
from typing import List

class DocTagsDAO:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def add_tags_to_doc(self, doc_id: int, tag_list: List[str]) -> None:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            for tag in tag_list:
                cursor.execute("INSERT OR IGNORE INTO doc_tags (doc_id, tag) VALUES (?, ?)", (doc_id, tag))
            connection.commit()
        except Exception as e:
            raise RuntimeError(f"An error occurred while adding tags to document: {e}")


    def get_doc_tags(self, doc_id: int) -> List[str]:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT tag FROM doc_tags WHERE doc_id=?", (doc_id,))
            tags = [row[0] for row in cursor.fetchall()]
            return tags
        except Exception as e:
            raise RuntimeError(f"An error occurred while retrieving tags for document: {e}")


    def get_tag_docs(self, tag: str) -> List[int]:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT doc_id FROM doc_tags WHERE tag=?", (tag,))
            doc_ids = [row[0] for row in cursor.fetchall()]
            return doc_ids
        except Exception as e:
            raise RuntimeError(f"An error occurred while retrieving documents for tag: {e}")


    def remove_doc_tags(self, doc_id: int) -> None:
        connection = self.db_connection.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM doc_tags WHERE doc_id=?", (doc_id,))
            connection.commit()
        except Exception as e:
            raise RuntimeError(f"An error occurred while removing tags from document: {e}")

