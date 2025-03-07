from unittest import TestCase, main
from unittest.mock import patch, mock_open
from collections import defaultdict, Counter
import pickle
from bigram_pipeline import BigramPipeline
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

    ## ---------- TEST: update_bigrams with Multiple Paragraphs ----------
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    @patch("pickle.dump")
    def test_update_bigrams_multiple_paragraphs(self, mock_pickle_dump, mock_exists, mock_file):
        """Test bigram updates across multiple paragraphs."""
        test_paragraphs = """Hello world. Good morning.

        This is a test paragraph. Another sentence in this paragraph.

        A second paragraph starts here. It also has sentences."""

        self.pipeline.update_bigrams(test_paragraphs)

        # Check bigram existence across multiple paragraphs
        self.assertIn("hello", self.pipeline.model)
        self.assertIn("world", self.pipeline.model["hello"])
        self.assertEqual(self.pipeline.model["hello"]["world"], 1)

        self.assertIn("this", self.pipeline.model)
        self.assertIn("is", self.pipeline.model["this"])
        self.assertEqual(self.pipeline.model["this"]["is"], 1)

        self.assertIn("a", self.pipeline.model)
        self.assertIn("test", self.pipeline.model["a"])
        self.assertEqual(self.pipeline.model["a"]["test"], 1)

        self.assertIn("a", self.pipeline.model)
        self.assertIn("second", self.pipeline.model["a"])
        self.assertEqual(self.pipeline.model["a"]["second"], 1)

        mock_pickle_dump.assert_called()  # Ensures model saving happens

    ## ---------- TEST: check_sentence with Multiple Paragraphs ----------
    def test_check_sentence_multiple_paragraphs(self):
        """Test sentence checking and ranking inside a Document with multiple paragraphs."""
        doc = Document(input_text="Hello world. Good morning.\n\nThis is a test paragraph. Another sentence.")

        doc.paragraphs = [
            # First paragraph
            type("Paragraph", (), {
                "sentences": [
                    type("Sentence", (), {
                        "tokens": [Token(source="world", suggestions={0: "earth", 1: "planet"})]
                    }),
                    type("Sentence", (), {
                        "tokens": [Token(source="morning", suggestions={0: "dawn", 1: "sunrise"})]
                    })
                ]
            })(),
            # Second paragraph
            type("Paragraph", (), {
                "sentences": [
                    type("Sentence", (), {
                        "tokens": [Token(source="test", suggestions={0: "trial", 1: "experiment"})]
                    }),
                    type("Sentence", (), {
                        "tokens": [Token(source="sentence", suggestions={0: "phrase", 1: "statement"})]
                    })
                ]
            })()
        ]

        self.pipeline.model["hello"]["world"] = 10
        self.pipeline.model["hello"]["earth"] = 5
        self.pipeline.model["hello"]["planet"] = 3

        self.pipeline.model["good"]["morning"] = 8
        self.pipeline.model["good"]["dawn"] = 4
        self.pipeline.model["good"]["sunrise"] = 2

        self.pipeline.model["this"]["test"] = 9
        self.pipeline.model["this"]["trial"] = 6
        self.pipeline.model["this"]["experiment"] = 4

        self.pipeline.model["another"]["sentence"] = 5
        self.pipeline.model["another"]["phrase"] = 3
        self.pipeline.model["another"]["statement"] = 2

        result = self.pipeline.check_sentence(doc)

        # Check ranking for "world"
        self.assertEqual(
            result["doc"].paragraphs[0].sentences[0].tokens[0].suggestions,
            {0: "world", 1: "earth", 2: "planet"}
        )

        # Check ranking for "morning"
        self.assertEqual(
            result["doc"].paragraphs[0].sentences[1].tokens[0].suggestions,
            {0: "morning", 1: "dawn", 2: "sunrise"}
        )

        # Check ranking for "test"
        self.assertEqual(
            result["doc"].paragraphs[1].sentences[0].tokens[0].suggestions,
            {0: "test", 1: "trial", 2: "experiment"}
        )

        # Check ranking for "sentence"
        self.assertEqual(
            result["doc"].paragraphs[1].sentences[1].tokens[0].suggestions,
            {0: "sentence", 1: "phrase", 2: "statement"}
        )


if __name__ == "__main__":
    main()
