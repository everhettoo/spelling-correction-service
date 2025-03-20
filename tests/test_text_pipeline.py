from unittest import TestCase

from app_config import Configuration
from models.document import Document
from models.token import Token
from models.types import WordType
from pipeline import text_pipeline
from tests import test_data


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        config = Configuration()
        cls.pipeline = text_pipeline.TextPipeline(config = config)

    def test_parse(self):
        doc = Document(test_data.sample_text1)
        # pipeline = text_pipeline.TextPipeline()
        self.pipeline.parse_doc(doc)

        # Sample_text1 has 2 paragraphs
        # paragraph-1 has 2 sentences. Paragraph-2 has a sentence.
        self.assertEqual(len(doc.paragraphs), 2)

        i = 0
        for paragraph in doc.paragraphs:
            if i == 0:
                self.assertEqual(len(paragraph.sentences), 2)
            if i == 1:
                self.assertEqual(len(paragraph.sentences), 1)

            i = i + 1

    def test_detect_language_when_english(self):
        doc = Document(test_data.hello_world_en)

        # Test the private method.
        actual = self.pipeline._TextPipeline__detect_language_when_english(doc),
        self.assertTrue(actual)

    def test_detect_language_when_english_given_russian(self):
        doc = Document(test_data.hello_world_rs)

        # Test the private method.
        actual = self.pipeline._TextPipeline__detect_language_when_english(doc)
        self.assertFalse(actual)

    def test_detect_language_when_english_given_chinese(self):
        doc = Document(test_data.hello_world_ch)

        # Test the private method.
        actual = self.pipeline._TextPipeline__detect_language_when_english(doc)
        self.assertFalse(actual)

    def test_detect_language_when_english_given_mixed(self):
        doc = Document(test_data.hello_world_en +
                       test_data.hello_world_rs +
                       test_data.hello_world_rs)

        # Test the private method.
        actual = self.pipeline._TextPipeline__detect_language_when_english(doc)
        self.assertFalse(actual)

    def test_parse_token(self):
        token1 = Token('diabetis')

        # Test the private method.
        self.pipeline._TextPipeline__parse_token(token1)
        self.assertEqual(WordType.NON_WORD, token1.word_type)

        self.pipeline._TextPipeline__review_words(token1)
        self.assertEqual(WordType.NON_WORD, token1.word_type)
        self.assertEqual(2, len(token1.suggestions))

    def test_review_words_when_is_correct_word(self):
        # Doc is not required, token is sufficient.
        token = Token('beta')
        token.word_type = WordType.WORD

        # Test the private method.
        self.pipeline._TextPipeline__review_words(token)
        self.assertEqual(len(token.suggestions), 0)

    def test_review_words_when_is_non_word(self):
        # Doc is not required, token is sufficient.
        # suggested: yellow, hollow, hello
        token = Token('glacoma')
        token.word_type = WordType.NON_WORD

        # Test the private method.
        self.pipeline._TextPipeline__review_words(token)
        self.assertEqual(len(token.suggestions), 1)
        self.assertEqual('glaucoma',token.suggestions[0])
