from unittest import TestCase

from models.document import Document
from tests import test_data


class TestDocument(TestCase):
    def test_parse(self):
        doc = Document(test_data.sample_text1)
        doc.parse_doc()

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
