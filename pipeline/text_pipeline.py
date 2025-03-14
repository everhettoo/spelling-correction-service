# This module handles:
# 1. language encoding and language detection
# 2. word tokenization (word segmentation)
import string

import chardet
import spacy
from nltk import edit_distance
from nltk.corpus import stopwords, words, PlaintextCorpusReader
from nltk.tokenize import word_tokenize, sent_tokenize
from spacy.tokenizer import Tokenizer

from app_config import Configuration
from models.document import Document
from models.paragraph import Paragraph
from models.sentence import Sentence
from models.token import Token
from models.types import WordType
from spacy.lang.en import English

class TextPipeline:
    def __init__(self, config: Configuration):
        self.err = False
        self.err_msg = ''
        self.stop_words = set(stopwords.words('english'))
        # words.fileids() --> ['en', 'en-basic']
        # self.corpus = set([item for item in words.words('en-basic') if item not in stopwords.words('english')])
        # corpus_dir = config.config_values['corpus_medical']
        # self.corpus = PlaintextCorpusReader(config.config_values['corpus_medical_dir'], '.*\.txt')
        self.corpus = PlaintextCorpusReader(config.config_values['corpus_medical_dir'],
                                            config.config_values['corpus_medical_name'])
        self.corpus = self.corpus.words()
        self.spacy_nlp = spacy.load("en_core_web_sm")
        self.nlp = English()
        self.common_contractions = {"can't": "cannot", "won't": "will not", "isn't": "is not", "you're": "you are", "I'm": "I am", "they've": "they have", "he's": "he is", "she'd": "she would", "we'll": "we will"}

    def execute_asc_pipeline(self, doc: Document):
        try:
            # self.__detect_language_when_english()
            self.parse_doc(doc)
        except Exception as e:
            self.err = True
            self.err_msg = str(e)

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
                tokenizer = Tokenizer(self.nlp.vocab)
                word_list = tokenizer(s)

                for word in word_list:
                    # Process token
                    print(word.pos_)
                    token = Token(str(word))
                    self.__review_words(token)
                    sentence.tokens.append(token)

                new_sentence = Sentence()

                for token in sentence.tokens:
                    if token.word_type == WordType.CONTRACTION:
                        tokens = token.source.split("'")
                        token_0 = Token(tokens[0])
                        token_0.word_type = WordType.WORD
                        token_1 = Token("'"+tokens[1])
                        token_1.word_type = WordType.CONTRACTION
                        new_sentence.tokens.append(token_0)
                        new_sentence.tokens.append(token_1)
                    elif token.word_type == WordType.POSSESSION:
                        tokens = token.source.split("'")
                        token_0 = Token(tokens[0])
                        token_0.word_type = WordType.WORD
                        token_0.suggestions = token.suggestions
                        token_1 = Token("'"+tokens[1])
                        token_1.word_type = WordType.POSSESSION
                        new_sentence.tokens.append(token_0)
                        new_sentence.tokens.append(token_1)
                    else:
                        new_sentence.tokens.append(token)

                # Add processed sentence (+tokens) into a new paragraph.
                paragraph.sentences.append(new_sentence)

            # Add the new paragraph into document.
            doc.paragraphs.append(paragraph)

    # TODO: check it is required or not
    def __detect_language_when_english(self, doc: Document):
        # TODO: To implement the logic.
        input_text = doc.input_text.encode()
        result = chardet.detect(input_text)['encoding']
        if result == 'ascii':
            return True
        else:
            return False

    # TODO: check it is required or not
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
        if token.source in self.common_contractions.keys():
            token.word_type = WordType.CONTRACTION
            return
        elif "'" in token.source.lower():
            token.word_type = WordType.POSSESSION
            new_words = token.source.split("'")
            new_word = new_words[0]
            i = 0
            for w in self.corpus:
                if w in token.suggestions.values():
                    continue

                m = edit_distance(new_word, w)
                if m == 1:
                    token.suggestions[i] = w
                    i = i + 1
            return
        elif token.source.lower() in string.punctuation:
            token.word_type = WordType.PUNCTUATION
            return
        elif token.source.lower() in self.stop_words:
            token.word_type = WordType.STOP_WORD
            return
        elif token.source.lower() in self.corpus:
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
