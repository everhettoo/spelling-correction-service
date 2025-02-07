from unittest import TestCase

from pipeline import text_preprocessor


class Test(TestCase):
    def test_detect_language_when_english(self):
        self.assertTrue(text_preprocessor.detect_language_when_english('Hello World'))

    def test_detect_language_when_english_given_russian(self):
        self.assertFalse(text_preprocessor.detect_language_when_english('Привет, мир'))

    def test_detect_language_when_english_given_chinese(self):
        self.assertFalse(text_preprocessor.detect_language_when_english('你好世界'))

    def test_detect_language_when_english_given_mixed(self):
        self.assertFalse(text_preprocessor.detect_language_when_english('Hello World Привет, мир 你好世界'))
