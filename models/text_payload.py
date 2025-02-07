from exceptiongroup import catch

from pipeline import text_preprocessor


class TextPayload:
    def __init__(self, text: str):
        self.__text = text
        self.__error = False
        self.__error_msg = None
        self.__tokens = None
        self.__token_type = None
        self.__token_count = -1

    def get_text(self):
        return self.__text

    def set_error(self, msg):
        self.__error = True
        self.__error_msg = msg

    def get_error(self):
        return self.__error

    def get_error_msg(self, msg):
        self.__error_msg = msg

    def get_payload(self):
        return self

    def detect_language(self):
        pass

    def detect_text(self):
        pass

    def tokenize_words(self):
        try:
            # Calls the pipeline for processing the input text.
            self.__tokens = text_preprocessor.tokenize_words(self.__text)
        except Exception as e:
            self.__error = True
            self.__error_msg = str(e)
