import faiss
import numpy as np

class VectorIndex:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(int(self.dimension))

    def add_embedding(self, embedding):
        embedding_np = np.array([embedding], dtype=np.float32)
        self.index.add(embedding_np)
        return self.index.ntotal

    def remove_embedding(self, id):
        # Placeholder: FAISS IndexFlatL2 does not support direct removal by ID.
        # Implement if using a different FAISS index type that supports removal.
        pass

    def search(self, query_embedding, k=10):
        query_np = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_np, k)
        return indices[0], distances[0]
