from unittest import TestCase

from models.document import Document
from models.token import Token
from pipeline import text_pipeline
from tests import test_data


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = text_pipeline.TextPipeline()

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

    def test_review_words_when_is_correct_word(self):
        # Doc is not required, token is sufficient.
        token = Token('hello')

        # Test the private method.
        self.pipeline._TextPipeline__review_words(token)
        self.assertEqual(len(token.suggestions), 0)

    def test_review_words_when_is_non_word(self):
        # Doc is not required, token is sufficient.
        # suggested: bellow, fellow, hallow, hello, hollow, mellow,yellow,hollow
        token = Token('hellow')

        # Test the private method.
        # {0: 'bellow', 1: 'fellow', 2: 'hallow', 3: 'hello', 4: 'hollow', 5: 'mellow', 6: 'yellow'}
        self.pipeline._TextPipeline__review_words(token)
        self.assertEqual(len(token.suggestions), 7)
