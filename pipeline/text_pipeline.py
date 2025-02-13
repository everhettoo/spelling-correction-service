# This module handles:
# 1. language encoding and language detection
# 2. word tokenization (word segmentation)
from nltk import ngrams, edit_distance
from nltk.corpus import words
from nltk.tokenize import word_tokenize
import chardet

from models.document import Document


class TextPipeline:
    def __init__(self, doc: Document):
        self.err = False
        self.err_msg = ''
        self.doc = doc
        # TODO: Need to remove or replace with custom corpus.
        self.correct_words = words.words()

    def execute_asc_pipeline(self):
        try:
            # self.__detect_language_when_english()
            self.doc.parse_doc()
        except Exception as e:
            self.err = True
            self.err_msg = str(e)
        finally:
            self.doc.input_text = ''

    #
    # def review(self):
    #     # TODO: Dummy method need to be revised!
    #     i = 0
    #     for word in self.tokens:
    #         i = i + 1
    #         word = Token(word)
    #         word.word_type = WordType.WORD
    #
    #         if i % 2 == 0:
    #             word.suggestions[1] = "asa1"
    #             word.suggestions[2] = "asa2"
    #             self.article.append(word)
    #             continue
    #
    #         self.article.append(word)

    def __detect_language_when_english(self):
        # TODO: To implement the logic.
        input_text = self.doc.input_text.encode()
        result = chardet.detect(input_text)['encoding']
        if result == 'ascii':
            return True
        else:
            return False

    def __tokenize_words(self):
        """
        This method tokenizes the text and returns tokens when no error occurs.
        :param: the input string.
        :return: list of strings as tokens.
        """
        try:
            tokens = word_tokenize(self.doc.input_text)
            # TODO: Need more careful handling where lib misses few words like bart's. Custom expression??

            return tokens
        except Exception as e:
            raise e

    def __review_words(self, token: str):
        m = edit_distance('help', 'helping')
        print(m)
        # list of incorrect spellings
        # that need to be corrected
        # incorrect_words = ['happpy', 'azmaing', 'intelliengt']
        # incorrect_words = ['hellow']

        # loop for finding correct spellings
        # based on edit distance and
        # printing the correct words
        # for word in token:
        # temp = [(edit_distance(token, w), w) for w in self.correct_words if w[0] == token]
        # print(sorted(temp, key=lambda val: val[0])[0][1])

        suggestion = []
        for w in self.correct_words:
            if w == token:
                break
            else:
                m = edit_distance(token, w)
                if m == 1:
                    suggestion.append(w)
