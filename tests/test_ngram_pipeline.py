import os

from unittest import TestCase
from collections import defaultdict, Counter
from pipeline.ngram_pipeline import NgramPipeline

class TestNgramPipeline(TestCase):
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests."""
        cls.model_path = "test_ngram_model.pkl"
        cls.ngram_pipeline = NgramPipeline(n=2, model_path=cls.model_path)

    def setUp(self):
        """Runs before each test to reset the model."""
        self.ngram_pipeline.model = defaultdict(Counter)  # Reset model

    def test_load_model(self):
        """Test if the model loads correctly as a defaultdict."""
        model = self.ngram_pipeline.load_model()
        self.assertIsInstance(model, defaultdict)
        self.assertIsInstance(model.default_factory(), Counter)

    def test_nlp_preprocess(self):
        """Test sentence preprocessing."""
        raw_text = "Hello, World! NLP is awesome."
        processed_text = self.ngram_pipeline.nlp_preprocess(raw_text)
        self.assertIsInstance(processed_text, str)
        self.assertTrue("hello" in processed_text.lower())  # Should be lowercase

    def test_tokenize(self):
        """Test if tokenization works as expected."""
        sentence = "Hello world NLP is great"
        tokens = self.ngram_pipeline.tokenize(sentence)
        self.assertEqual(tokens, ["Hello", "world", "NLP", "is", "great"])

    def test_build_model(self):
        """Test n-gram model building from tokens."""
        tokens = ["hello", "world", "this", "is", "a", "test"]
        self.ngram_pipeline.build_model(tokens)

        self.assertIn(("hello",), self.ngram_pipeline.model)
        self.assertEqual(self.ngram_pipeline.model[("hello",)]["world"], 1)

        self.assertIn(("this",), self.ngram_pipeline.model)
        self.assertEqual(self.ngram_pipeline.model[("this",)]["is"], 1)

    def test_preprocess_build_model(self):
        """Test the full pipeline: preprocessing, tokenization, and model update."""
        sentence = "Hello world, this is an n-gram test."
        self.ngram_pipeline.preprocess_build_model(sentence)

        self.assertIn(("hello",), self.ngram_pipeline.model)
        self.assertGreater(self.ngram_pipeline.model[("hello",)]["world"], 0)

    def test_save_and_reload_model(self):
        """Test saving and reloading the n-gram model."""
        self.ngram_pipeline.preprocess_build_model("This is a test sentence for saving.")
        self.ngram_pipeline.save_model()

        new_pipeline = NgramPipeline(n=2, model_path=self.model_path)
        self.assertNotEqual(new_pipeline.model, defaultdict(Counter))  # Ensure model loaded
        self.assertIn(("this",), new_pipeline.model)
        self.assertGreater(new_pipeline.model[("this",)]["is"], 0)

    @classmethod
    def tearDownClass(cls):
        """Clean up the test model file after all tests are run."""
        if os.path.exists(cls.model_path):
            os.remove(cls.model_path)

if __name__ == "__main__":
    unittest.main()
