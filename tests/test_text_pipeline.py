from unittest import TestCase

from models.document import Document
from pipeline import text_pipeline
from tests import test_data


class Test(TestCase):
    def test_detect_language_when_english(self):
        doc = Document(test_data.hello_world_en)
        pipeline = text_pipeline.TextPipeline(doc)

        # Test the private method.
        actual = pipeline._TextPipeline__detect_language_when_english(),
        self.assertTrue(actual)

    def test_detect_language_when_english_given_russian(self):
        doc = Document(test_data.hello_world_rs)
        pipeline = text_pipeline.TextPipeline(doc)

        # Test the private method.
        actual = pipeline._TextPipeline__detect_language_when_english()
        self.assertFalse(actual)

    def test_detect_language_when_english_given_chinese(self):
        doc = Document(test_data.hello_world_ch)
        pipeline = text_pipeline.TextPipeline(doc)

        # Test the private method.
        actual = pipeline._TextPipeline__detect_language_when_english()
        self.assertFalse(actual)

    def test_detect_language_when_english_given_mixed(self):
        doc = Document(test_data.hello_world_en +
                       test_data.hello_world_rs +
                       test_data.hello_world_rs)
        pipeline = text_pipeline.TextPipeline(doc)

        # Test the private method.
        actual = pipeline._TextPipeline__detect_language_when_english()
        self.assertFalse(actual)

    def test___review_words(self):
        doc = Document(test_data.hello_world_en +
                       test_data.hello_world_rs +
                       test_data.hello_world_rs)
        pipeline = text_pipeline.TextPipeline(doc)

        # Test the private method.
        actual = pipeline._TextPipeline__review_words('hello')
        self.assertFalse(actual)
