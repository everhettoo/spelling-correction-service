# This module handles:
# 1. language encoding and language detection
# 2. word tokenization (word segmentation)
import string

import chardet
from nltk import edit_distance
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize, sent_tokenize

from models.document import Document
from models.paragraph import Paragraph
from models.sentence import Sentence
from models.token import Token
from models.types import WordType


class TextPipeline:
    def __init__(self):
        self.err = False
        self.err_msg = ''
        self.stop_words = set(stopwords.words('english'))
        self.corpus = set([item for item in words.words() if item not in stopwords.words('english')])

    def execute_asc_pipeline(self, doc: Document):
        try:
            # self.__detect_language_when_english()
            self.parse_doc(doc)
        except Exception as e:
            self.err = True
            self.err_msg = str(e)
        finally:
            doc.input_text = ''

    def parse_doc(self, doc: Document):
        doc.paragraphs = []
        paragraph_list = doc.input_text.split("\r\n")
        for p in paragraph_list:
            # Process paragraph
            paragraph = Paragraph()
            sentence_list = sent_tokenize(p)
            for s in sentence_list:
                # Process sentence
                sentence = Sentence()
                word_list = word_tokenize(s)
                for word in word_list:
                    # Process token
                    token = Token(word)
                    self.__review_words(token)
                    sentence.tokens.append(token)

                # Add processed sentence (+tokens) into a new paragraph.
                paragraph.sentences.append(sentence)

            # Add the new paragraph into document.
            doc.paragraphs.append(paragraph)

    def __detect_language_when_english(self, doc: Document):
        # TODO: To implement the logic.
        input_text = doc.input_text.encode()
        result = chardet.detect(input_text)['encoding']
        if result == 'ascii':
            return True
        else:
            return False

    def __tokenize_words(self, doc: Document):
        """
        This method tokenizes the text and returns tokens when no error occurs.
        :param: the input string.
        :return: list of strings as tokens.
        """
        try:
            tokens = word_tokenize(doc.input_text)
            # TODO: Need more careful handling where lib misses few words like bart's. Custom expression??

            return tokens
        except Exception as e:
            raise e

    def __review_words(self, token: Token):
        token.suggestions = dict()

        if token.source in string.punctuation:
            token.word_type = WordType.PUNCTUATION
            return
        if token.source.lower() in self.stop_words:
            token.word_type = WordType.STOP_WORD
            return
        if token.source.lower() in self.corpus:
            token.word_type = WordType.WORD
            return

        i = 0
        for w in self.corpus:
            # TODO: Not sure why same word repeats twice.
            if w in token.suggestions.values():
                continue

            m = edit_distance(token.source.lower(), w)
            if m == 1:
                token.suggestions[i] = w
                i = i + 1
