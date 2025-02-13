# This class holds each token and the autocorrected words.
from models.types import WordType


class Token:
    def __init__(self, word):
        self.source = word
        self.word_type = WordType.UNDEFINED
        self.suggestions = dict()
