import unittest
from src.ragtag.db.vector_index import VectorIndex
import numpy as np

class TestVectorIndex(unittest.TestCase):
    def setUp(self):
        self.vector_index = VectorIndex(dimension=128)
        self.sample_embedding = np.random.rand(128).astype('float32')

    def test_add_embedding(self):
        initial_count = self.vector_index.index.ntotal
        self.vector_index.add_embedding(self.sample_embedding)
        self.assertEqual(self.vector_index.index.ntotal, initial_count + 1, "Embedding should be added to the index")

    def test_search_embedding(self):
        self.vector_index.add_embedding(self.sample_embedding)
        results = self.vector_index.search(self.sample_embedding, k=1)
        self.assertTrue(len(results) > 0, "Search should return at least one result")

    # def test_remove_embedding(self):
    #     self.vector_index.add_embedding(self.sample_embedding)
    #     initial_count = self.vector_index.index.ntotal
    #     self.vector_index.remove_embedding(self.sample_embedding)
    #     self.assertEqual(self.vector_index.index.ntotal, initial_count - 1, "Embedding should be removed from the index")

if __name__ == '__main__':
    unittest.main()
