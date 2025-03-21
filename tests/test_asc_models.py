from unittest import TestCase

from app_config import Configuration
from models.document import Document
from models.types import WordType
from pipeline.bigram_pipeline import BigramPipeline
from pipeline.text_pipeline import TextPipeline


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        config = Configuration()
        cls.pipeline = TextPipeline(config=config)
        cls.bigram = BigramPipeline()

    def assert_token_type(self, doc: Document, data: dict):
        for paragraph in doc.paragraphs:
            for sentence in paragraph.sentences:
                for token in sentence.tokens:
                    for k, v in data.items():
                        if token.source == k:
                            self.assertEqual(token.word_type, v)

    def test_for_no_error_sentence(self):
        data = {'Neonatal': WordType.WORD,
                'is': WordType.STOP_WORD,
                'a': WordType.STOP_WORD,
                'diabetes': WordType.WORD,
                'of': WordType.STOP_WORD,
                'mellitus': WordType.WORD,
                '.': WordType.PUNCTUATION}
        doc = Document('Neonatal is a diabetes of mellitus.')
        # Parse the tokens for marking (no non-word or real-word marking yet, only word).
        self.pipeline.parse_doc(doc)

        # Now, the marking on spelling error type applied.
        self.bigram.verify_error_type(doc, self.pipeline.corpus)
        self.assert_token_type(doc, data)

        # Now, perform edit-distance on non-word and noisy-channel on word,

        for paragraph in doc.paragraphs:
            for sentence in paragraph.sentences:
                for token in sentence.tokens:
                    self.pipeline._TextPipeline__review_words(token)

        self.assert_token_type(doc, data)

    def test_for_non_and_real_word_error_sentence(self):
        data = {'Neonatal': WordType.WORD,
                'is': WordType.STOP_WORD,
                'a': WordType.STOP_WORD,
                'diabetis': WordType.NON_WORD,
                'of': WordType.STOP_WORD,  # Since the previous word becomes non-word, this becomes real-word
                'mellitus': WordType.REAL_WORD,
                '.': WordType.PUNCTUATION}
        doc = Document('Neonatal is a diabetis of mellitus.')
        # Parse the tokens for marking (no non-word or real-word marking yet, only word).
        self.pipeline.parse_doc(doc)

        # Now, the marking on spelling error type applied.
        self.bigram.verify_error_type(doc, self.pipeline.corpus)
        self.assert_token_type(doc, data)

        # Now, perform edit-distance on non-word and noisy-channel on word,
        for paragraph in doc.paragraphs:
            for sentence in paragraph.sentences:
                for token in sentence.tokens:
                    self.pipeline._TextPipeline__review_words(token)

        self.assert_token_type(doc, data)

    def test_for_no_error_sentence_with_pipeline(self):
        data = {'Neonatal': WordType.WORD,
                'is': WordType.STOP_WORD,
                'a': WordType.STOP_WORD,
                'diabetes': WordType.WORD,
                'of': WordType.STOP_WORD,
                'mellitus': WordType.WORD,
                '.': WordType.PUNCTUATION}
        doc = Document('Neonatal is a diabetes of mellitus.')
        self.pipeline.execute_asc_pipeline(doc)
        self.assert_token_type(doc, data)

    def test_for_non_and_real_word_error_sentence_with_pipeline(self):
        data = {'Neonatal': WordType.WORD,
                'is': WordType.STOP_WORD,
                'a': WordType.STOP_WORD,
                'diabetis': WordType.NON_WORD,
                'of': WordType.STOP_WORD,  # Since the previous word becomes non-word, this becomes real-word
                'mellitus': WordType.REAL_WORD,
                '.': WordType.PUNCTUATION}
        doc = Document('Neonatal is a diabetis of mellitus.')
        self.pipeline.execute_asc_pipeline(doc)
        self.assert_token_type(doc, data)

