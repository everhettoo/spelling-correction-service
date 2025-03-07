from unittest import TestCase, main
from unittest.mock import patch, mock_open
from collections import defaultdict, Counter
import pickle
from pipeline.bigram_pipeline import BigramPipeline  # ✅ Correct import
from models.document import Document
from models.token import Token


class TestBigramPipeline(TestCase):

    def setUp(self):
        """Set up a BigramPipeline instance with a mock model."""
        self.pipeline = BigramPipeline()
        self.pipeline.model = defaultdict(Counter, {
            "hello": Counter({"world": 5, "there": 3, "friend": 7}),
            "good": Counter({"morning": 10, "afternoon": 2}),
            "this": Counter({"is": 8, "a": 5}),
            "a": Counter({"test": 6, "paragraph": 3})
        })

    ## ---------- TEST: Model Loading ----------
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    @patch("pickle.load", return_value=defaultdict(Counter, {"hello": Counter({"world": 3})}))
    def test_load_model(self, mock_pickle_load, mock_open_file, mock_exists):
        """Test that the model loads correctly when a valid file exists."""
        pipeline = BigramPipeline()
        self.assertEqual(pipeline.model["hello"]["world"], 3)

    ## ---------- TEST: Saving Model ----------
    @patch("builtins.open", new_callable=mock_open)
    @patch("pickle.dump")
    def test_save_model(self, mock_pickle_dump, mock_file):
        """Test that the model saves without errors."""
        self.pipeline.save_model()
        mock_pickle_dump.assert_called_once()

    ## ---------- TEST: Cleaning Text ----------
    @patch("utils.regex.remove_url", return_value="clean text")
    @patch("utils.regex.remove_html", return_value="clean text")
    @patch("utils.regex.remove_bracketed_text", return_value="clean text")
    @patch("utils.regex.transform_contractions", return_value="clean text")
    def test_clean_text(self, mock_transform, mock_brackets, mock_html, mock_url):
        """Test that text cleaning applies all regex functions."""
        result = self.pipeline.clean_text("Sample text with [info].")
        self.assertEqual(result, "clean text")

    ## ---------- TEST: Convert Multi-Paragraph & Multi-Sentence ----------
    @patch("pipeline.bigram_pipeline.BigramPipeline.nlp_preprocess", return_value="processed sentence")
    def test_convert2sentences_multi_paragraphs(self, mock_nlp):
        """Test conversion of multi-paragraph text into sentences."""
        text = "Hello world. Good morning.\n\nThis is a test paragraph. Another sentence follows."
        expected = ["processed sentence", "processed sentence", "processed sentence", "processed sentence"]
        result = self.pipeline.convert2sentences(text)
        self.assertEqual(result, expected)

    ## ---------- TEST: Tokenization ----------
    def test_tokenize(self):
        """Test basic tokenization."""
        result = self.pipeline.tokenize("Hello world!")
        self.assertEqual(result, ["hello", "world", "!"])

    ## ---------- TEST: rank_suggestions ----------
    def test_rank_suggestions_basic(self):
        """Test ranking of suggestions based on frequency."""
        suggestions = {0: "world", 1: "there", 2: "friend"}
        expected = {0: "friend", 1: "world", 2: "there"}  # Sorted by frequency (7, 5, 3)
        result = self.pipeline.rank_suggestions("hello", suggestions)
        self.assertEqual(result, expected)

    ## ---------- TEST: update_bigrams with Multi-Paragraphs ----------
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    @patch("pickle.dump")
    def test_update_bigrams_multi_paragraphs(self, mock_pickle_dump, mock_exists, mock_file):
        """Test bigram updates across multiple paragraphs."""
        test_text = """Hello world. Good morning.

        This is a test paragraph. Another sentence in this paragraph.

        A second paragraph starts here. It also has sentences."""

        self.pipeline.update_bigrams(test_text)

        self.assertIn("hello", self.pipeline.model)
        self.assertIn("world", self.pipeline.model["hello"])
        self.assertEqual(self.pipeline.model["hello"]["world"], 6)

        self.assertIn("this", self.pipeline.model)
        self.assertIn("is", self.pipeline.model["this"])
        self.assertEqual(self.pipeline.model["this"]["is"], 8)

        self.assertIn("a", self.pipeline.model)
        self.assertIn("test", self.pipeline.model["a"])
        self.assertEqual(self.pipeline.model["a"]["test"], 6)

        mock_pickle_dump.assert_called()  # Ensures model saving happens

    ## ---------- TEST: check_sentence with Multi-Paragraphs ----------
    def test_check_sentence_multi_paragraphs(self):
        """Test sentence checking and ranking inside a Document with multiple paragraphs."""
        doc = Document(input_text="Hello world. Good morning.\n\nThis is a test paragraph. Another sentence.")

        doc.paragraphs = [
            type("Paragraph", (), {
                "sentences": [
                    type("Sentence", (), {
                        "tokens": [Token("world")]
                    }),
                    type("Sentence", (), {
                        "tokens": [Token("morning")]
                    })
                ]
            })(),
            type("Paragraph", (), {
                "sentences": [
                    type("Sentence", (), {
                        "tokens": [Token("test")]
                    }),
                    type("Sentence", (), {
                        "tokens": [Token("sentence")]
                    })
                ]
            })()
        ]

        # Assign suggestions manually
        doc.paragraphs[0].sentences[0].tokens[0].suggestions = {0: "earth", 1: "planet"}
        doc.paragraphs[0].sentences[1].tokens[0].suggestions = {0: "dawn", 1: "sunrise"}
        doc.paragraphs[1].sentences[0].tokens[0].suggestions = {0: "trial", 1: "experiment"}
        doc.paragraphs[1].sentences[1].tokens[0].suggestions = {0: "phrase", 1: "statement"}

        result = self.pipeline.check_sentence(doc)

        # Check ranking for "world"
        self.assertEqual(
            result["doc"].paragraphs[0].sentences[0].tokens[0].suggestions,
            {0: "earth", 1: "planet"}
        )

        # Check ranking for "morning"
        self.assertEqual(
            result["doc"].paragraphs[0].sentences[1].tokens[0].suggestions,
            {0: "dawn", 1: "sunrise"}
        )

        # Check ranking for "test"
        self.assertEqual(
            result["doc"].paragraphs[1].sentences[0].tokens[0].suggestions,
            {0: "trial", 1: "experiment"}
        )

        # Check ranking for "sentence"
        self.assertEqual(
            result["doc"].paragraphs[1].sentences[1].tokens[0].suggestions,
            {0: "phrase", 1: "statement"}
        )


if __name__ == "__main__":
    main()
