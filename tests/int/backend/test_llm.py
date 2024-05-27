import unittest

from src.backend.llm import generate_embedding_for_text, generate_tags_for_text, EMBEDDING_SIZE

class TestLLMFunctions(unittest.TestCase):
    def test_generate_embedding_for_text(self):
        sample_text = "This is a test."
        embedding = generate_embedding_for_text(sample_text)
        self.assertIsInstance(embedding, list)
        # Assuming 128-dimensional embedding with 4 bytes per float
        self.assertEqual(len(embedding), EMBEDDING_SIZE)

    def test_generate_tags_for_text(self):
        sample_text = "Python is a high-level, interpreted programming language."
        tags = generate_tags_for_text(sample_text)
        self.assertTrue(len(tags))
        self.assertTrue( "python" in tags )
        self.assertIsInstance(tags, list)
        self.assertTrue(all(isinstance(tag, str) for tag in tags))

if __name__ == '__main__':
    unittest.main()
