from typing import List

from models.token import Token


class Sentence:
    def __init__(self):
        self.tokens: List[Token] = []
