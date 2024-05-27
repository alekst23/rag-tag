import numpy as np
from typing import List

from src.db.document_dao import DocumentDAO
from src.db.tags_dao import TagsDAO
from src.db.doc_tags_dao import DocTagsDAO
from .llm import generate_tags_for_text, generate_embedding_for_text, EMBEDDING_SIZE
from src.db.vector_index import VectorIndex


class RagTag:
    def __init__(self, db_connection):
        """
        Initializes the RagTag system with a database connection.
        """
        self.vector_index = VectorIndex(dimension=EMBEDDING_SIZE)

        self.db_connection = db_connection
        self.document_dao = DocumentDAO(db_connection)
        self.tags_dao = TagsDAO(db_connection, self.vector_index)
        self.doc_tags_dao = DocTagsDAO(db_connection)

    def add_document(self, document_text):
        """
        Adds a single document to the store. Generates tags for the document using GPT-3.
        """
        document_id = self.document_dao.create_document(document_text)
        
        if document_id:
            tags = generate_tags_for_text(document_text)
            [self._ensure_tag_exists(tag) for tag in tags]
            
            self.doc_tags_dao.add_tags_to_doc(document_id, tags)
        
        return document_id

    def add_documents_bulk(self, documents: List[str]):
        """
        Adds multiple documents to the store in a bulk operation. Generates tags for each document.
        """
        document_ids = []
        for document_text in documents:
            document_id = self.add_document(document_text)
            document_ids.append(document_id)
        return document_ids

    def _ensure_tag_exists(self, tag: str) -> int:
        """
        Checks if a tag exists, adds it if not, and returns the tag ID.
        """
        existing_tag = self.tags_dao.get_tag(tag)
        if existing_tag:
            return existing_tag[0]
        else:
            return self._create_new_tag(tag)

    def _create_new_tag(self, tag: str) -> int:
        """
        Creates a new tag in the database and returns the tag ID.
        """
        # generate embedding
        embedding = generate_embedding_for_text(tag)

        # store vector
        faiss_id = self.vector_index.add_embedding(embedding)

        # store tag
        return self.tags_dao.add_tag(tag, embedding, faiss_id)

    # Additional methods and logic as required by the project
