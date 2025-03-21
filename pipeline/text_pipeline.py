# This module handles:
# 1. language encoding and language detection
# 2. word tokenization (word segmentation)
# 3. Noisy-channel
# 4. Edit-distance
import string

import chardet
import spacy
from nltk import edit_distance
from nltk.corpus import stopwords, PlaintextCorpusReader
from nltk.tokenize import word_tokenize, sent_tokenize
from spacy.tokenizer import Tokenizer

from app_config import Configuration
from models.document import Document
from models.paragraph import Paragraph
from models.sentence import Sentence
from models.token import Token
from models.types import WordType
from noisy_channel.channel_v1 import ChannelV1, datafile
from noisy_channel.proba_distributor import ProbaDistributor
from pipeline.bigram_pipeline import BigramPipeline
from utils.duration import Timer


class TextPipeline:
    def __init__(self, config: Configuration):
        self.err = False
        self.err_msg = ''
        self.stop_words = set(stopwords.words('english'))

        self.corpus = PlaintextCorpusReader(config.config_values['corpus_medical_dir'],
                                            config.config_values['corpus_medical_name'])
        self.corpus = self.corpus.words()
        # self.spacy_nlp = spacy.load("en_core_web_sm")
        self.nlp = spacy.load("en_core_web_sm")
        # self.nlp = English()
        self.common_contractions = {"can't": "cannot", "won't": "will not", "isn't": "is not", "you're": "you are",
                                    "I'm": "I am", "they've": "they have", "he's": "he is", "she'd": "she would",
                                    "we'll": "we will"}

        self.p_lang_model = ProbaDistributor(datafile(config.config_values['noisy_channel_word_file']))
        self.p_error_model = ProbaDistributor(datafile(config.config_values['noisy_channel_edit_file']))
        self.channel = ChannelV1(lang_model=self.p_lang_model,
                                 error_model=self.p_error_model,
                                 spell_error=(1. / 20.),
                                 alphabet='abcdefghijklmnopqrstuvwxyz')

        # Bi-gram processor for checking language model.
        self.bigram = BigramPipeline()

    def execute_asc_pipeline(self, doc: Document):
        try:
            self.__detect_language_when_english(doc)
            self.parse_doc(doc)
            self.bigram.verify_error_type(doc, self.corpus)
            self.review_doc(doc)
            self.bigram.check_sentence(doc)
        except Exception as e:
            self.err = True
            self.err_msg = str(e)

    def parse_doc(self, doc: Document):
        timer_para = Timer()
        doc.paragraphs = []
        paragraph_list = doc.input_text.split("\r\n")

        timer_para.start()
        print(f'[Text-Processor:Parse] - processing {len(paragraph_list)} paragraphs...')

        for p in paragraph_list:
            # Process paragraph
            paragraph = Paragraph()
            sentence_list = sent_tokenize(p)

            timer_sen = Timer()
            timer_sen.start()
            print(f'[Text-Processor:Parse] - processing {len(sentence_list)} sentences...')
            for s in sentence_list:
                # Process sentence
                sentence = Sentence()
                tokenizer = Tokenizer(self.nlp.vocab)
                word_list = tokenizer(s)

                timer_token = Timer()
                timer_token.start()
                print(f'[Text-Processor:Parse] - processing {len(word_list)} tokens...')
                for word in word_list:
                    # Parse token to relevant types:
                    token = Token(str(word))
                    tokens = self.__parse_token(token)
                    sentence.tokens.extend(tokens)

                print(f'[Text-Processor:Parse] - completed tokens in {timer_token.stop()} seconds.')
                # Add processed sentence (+tokens) into a new paragraph.
                paragraph.sentences.append(sentence)

            print(f'[Text-Processor:Parse] - completed sentences in {timer_sen.stop()} seconds.')
            # Add the new paragraph into document.
            doc.paragraphs.append(paragraph)

        print(f'[Text-Processor:Parse] - completed paragraphs in {timer_para.stop()} seconds.')

    def review_doc(self, doc: Document):
        timer_para = Timer()
        timer_para.start()
        print(f'[Text-Processor:Review] - processing paragraphs...')

        for paragraph in doc.paragraphs:
            for sentence in paragraph.sentences:
                timer_token = Timer()
                timer_token.start()
                print(f'[Text-Processor:Review] - processing {len(sentence.tokens)} tokens...')
                for token in sentence.tokens:
                    self.__review_words(token)

                print(f'[Text-Processor:Review] - completed tokens in {timer_token.stop()} seconds.')
        print(f'[Text-Processor:Review] - completed paragraphs in {timer_para.stop()} seconds.')

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

    def __parse_token(self, token: Token) -> list[Token]:
        token_list = []
        # TODO: This need to configured in the spacy rule for tokenization.
        if "." in token.source.lower() or "," in token.source.lower():
            token.word_type = WordType.UNDEFINED
        elif token.source in self.common_contractions.keys():
            token.word_type = WordType.CONTRACTION
        elif "'" in token.source.lower():
            token.word_type = WordType.APOSTROPHE
        elif token.source.lower() in string.punctuation:
            token.word_type = WordType.PUNCTUATION
        elif token.source.lower() in self.stop_words:
            token.word_type = WordType.STOP_WORD
        else:
            token.word_type = WordType.WORD

        if token.word_type == WordType.UNDEFINED:
            # TODO: This custom handling for '.' and ',' is a quick-fix for 'symptom+,' error.
            #  Two segments to remove '.' and ','
            # E.g. dance. and dr. albert
            # E.g. symptom,
            # Comma (,)
            if chr(44) in token.source:
                self.custom_symbol_handling(token, token_list, chr(44))
            #  Period (.)
            if chr(46) in token.source:
                self.custom_symbol_handling(token, token_list, chr(46))
        elif token.word_type == WordType.APOSTROPHE:
            # There must be two segments.
            word_list = token.source.split("'")
            token_0 = Token(word_list[0])
            token_1 = Token(word_list[1])

            # The first is labelled as word or non - word.
            token_0.word_type = WordType.WORD if word_list[0] in self.corpus else WordType.NON_WORD

            # Second is always the carrier.
            token_1.word_type = WordType.APOSTROPHE

            token_list.append(token_0)
            token_list.append(token_1)
        else:
            token_list.append(token)

        return token_list

    def custom_symbol_handling(self, token: Token, token_list, c):
        pos = token.source.index(c)
        if pos == len(token.source) - 1:
            token_0 = Token(token.source.replace(c, ''))
            token_0.word_type = WordType.WORD if token_0.source in self.corpus else WordType.NON_WORD
            token_1 = Token(c)
            token_1.word_type = WordType.PUNCTUATION
            token_list.append(token_0)
            token_list.append(token_1)
        else:
            # A name can be treated a single word.
            token.word_type = WordType.NON_WORD
            token_list.append(token)

    def __review_words(self, token: Token):
        token.suggestions = dict()

        if token.word_type == WordType.NON_WORD:
            self.__edit_distance(token)

        # Removing NON-WORD, only REAL-WORD checked in noisy-channel as per documentation.
        if token.word_type == WordType.REAL_WORD:
            self.__noisy_channel(token)

    def __edit_distance(self, token: Token):
        i = 0
        for w in self.corpus:
            if w in token.suggestions.values():
                continue

            m = edit_distance(token.source.lower(), w)
            if m == 1:
                token.suggestions[i] = w
                i = i + 1

    def __noisy_channel(self, token: Token):
        i = len(token.suggestions)
        c = self.channel.correct(token.source.lower())
        # print(c)
        # if c not in token.suggestions.values() and c != token.source.lower():
        # This means, two different words in the corpus identified through edits.
        if c != token.source.lower():
            token.suggestions[i] = c
            # token.type = WordType.REAL_WORD
