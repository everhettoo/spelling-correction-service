from models.types import WordType


class ReviewWord:
    def __init__(self, text):
        self.source = text
        self.word_type = WordType.OTHER
        self.suggestions = dict()


class ReviewResponse:
    def __init__(self, text, tokens):
        self.original_text = text
        self.tokens = tokens
        self.token_count = len(tokens)
        self.review_words = []

    def process(self):
        for word in self.tokens:
            word = ReviewWord(word)
            word.word_type = WordType.OTHER
            word.suggestions[1] = "asa1"
            word.suggestions[2] = "asa2"
            self.review_words.append(word)
