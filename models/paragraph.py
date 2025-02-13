from typing import List

from models.sentence import Sentence


class Paragraph:
    def __init__(self):
        self.sentences: List[Sentence] = []
