from unittest import TestCase

from app_config import Configuration
from models.document import Document
from models.token import Token
from pipeline import text_pipeline
from tests import test_data


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        config = Configuration()
        cls.pipeline = text_pipeline.TextPipeline(config = config)

    def test_parse(self):
        doc = Document(test_data.sample_text2)
        # pipeline = text_pipeline.TextPipeline()
        self.pipeline.parse_doc(doc)




