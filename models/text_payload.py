from models.types import WordType
from models.word_review import WordReview
from pipeline import text_preprocessor


class TextPayload:
    def __init__(self, text: str):
        self.text = text
        self.error = False
        self.error_msg = None
        self.tokens = None
        self.token_count = -1
        self.reviewed_words = []

    def tokenize_words(self):
        try:
            # Calls the pipeline for processing the input text.
            self.tokens = text_preprocessor.tokenize_words(self.text)
            self.token_count = len(self.tokens)
        except Exception as e:
            self.error = True
            self.error_msg = str(e)

    def review(self):
        for word in self.tokens:
            word = WordReview(word)
            word.word_type = WordType.UNDEFINED
            word.suggestions[1] = "asa1"
            word.suggestions[2] = "asa2"
            self.reviewed_words.append(word)
