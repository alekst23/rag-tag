import numpy as np
from typing import List

from src.db.document_dao import DocumentDAO
from src.db.tags_dao import TagsDAO
from src.db.doc_tags_dao import DocTagsDAO
from .llm import generate_tags_for_text, generate_embedding_for_text, EMBEDDING_SIZE
from src.db.vector_index import VectorIndex

SEARCH_THRESHOLD = 0.3

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

    def search_documents(self, query: str) -> List[str]:
        """
        Searches for documents based on a query string.
        """
        # Find matching tags
        q_embedding = generate_embedding_for_text(query)

        if not (vector_results := self.vector_index.search(q_embedding)):
            print("No matching vectors found")
            return []
        
        tag_scores = {}
        for faiss_id, distance in zip(*vector_results):
            if not (tag := self.tags_dao.get_tag_by_faiss_id(faiss_id)):
                continue
            if distance > SEARCH_THRESHOLD:
                continue
        
            tag_scores[tag] = 1 / (1+distance)


        # Get related docs into a matrix of tag -> doc_ids
        doc_matrix = {tag: self.doc_tags_dao.get_tag_docs(tag) for tag in tag_scores.keys()}

        # Fuse doc search results
        doc_scores = {}
        for tag, doc_ids in doc_matrix.items():
            for doc_id in doc_ids:
                doc_scores[doc_id] = doc_scores.get(doc_id, 0) + tag_scores[tag]

        # Sort by score
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_docs

        # 
    # Additional methods and logic as required by the project
