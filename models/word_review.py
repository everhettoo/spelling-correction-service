from models.types import WordType


class WordReview:
    def __init__(self, word):
        self.source = word
        self.word_type = WordType.UNDEFINED
        self.suggestions = dict()
