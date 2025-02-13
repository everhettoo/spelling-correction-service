from unittest import TestCase

from nltk.corpus import words

from models.document import Document
from pipeline import text_pipeline
from tests import test_data


class Test(TestCase):
    def test_parse(self):
        doc = Document(test_data.sample_text1)
        pipeline = text_pipeline.TextPipeline(words.words())
        pipeline.parse_doc(doc)

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
        pipeline = text_pipeline.TextPipeline(words.words())

        # Test the private method.
        actual = pipeline._TextPipeline__detect_language_when_english(doc),
        self.assertTrue(actual)

    def test_detect_language_when_english_given_russian(self):
        doc = Document(test_data.hello_world_rs)
        pipeline = text_pipeline.TextPipeline(doc)

        # Test the private method.
        actual = pipeline._TextPipeline__detect_language_when_english(doc)
        self.assertFalse(actual)

    def test_detect_language_when_english_given_chinese(self):
        doc = Document(test_data.hello_world_ch)
        pipeline = text_pipeline.TextPipeline(doc)

        # Test the private method.
        actual = pipeline._TextPipeline__detect_language_when_english(doc)
        self.assertFalse(actual)

    def test_detect_language_when_english_given_mixed(self):
        doc = Document(test_data.hello_world_en +
                       test_data.hello_world_rs +
                       test_data.hello_world_rs)
        pipeline = text_pipeline.TextPipeline(doc)

        # Test the private method.
        actual = pipeline._TextPipeline__detect_language_when_english(doc)
        self.assertFalse(actual)

    def test_review_words(self):
        doc = Document(test_data.hello_world_en +
                       test_data.hello_world_rs +
                       test_data.hello_world_rs)
        pipeline = text_pipeline.TextPipeline(doc)

        # Test the private method.
        actual = pipeline._TextPipeline__review_words('hello')
        self.assertFalse(actual)
