from typing import List

from models.paragraph import Paragraph


class Document:
    def __init__(self, input_text: str):
        self.input_text = input_text
        self.paragraphs: List[Paragraph] = []
