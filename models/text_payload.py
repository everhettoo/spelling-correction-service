from pipeline import text_preprocessor


class TextPayload:
    def __init__(self, text: str):
        self.text = text
        self.error = False
        self.error_msg = None
        self.tokens = None
        self.token_count = -1

    def tokenize_words(self):
        try:
            # Calls the pipeline for processing the input text.
            self.tokens = text_preprocessor.tokenize_words(self.text)
            self.token_count = len(self.tokens)
        except Exception as e:
            self.error = True
            self.error_msg = str(e)
