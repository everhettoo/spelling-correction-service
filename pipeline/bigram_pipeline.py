import nltk
import os
import pickle

from nltk.corpus import PlaintextCorpusReader

import utils.regex as rx

from collections import defaultdict, Counter
from importlib import reload
from nlppreprocess import NLP
from nltk import word_tokenize, sent_tokenize, bigrams
from models.document import Document
from models.types import WordType
from utils.duration import Timer

reload(rx)

nltk.download('punkt')  # Ensure NLTK tokenizer is available


class BigramPipeline:
    def __init__(self, model_path="data/bigram_freq.pkl"):
        self.err = False
        self.err_msg = ''
        self.model_path = model_path if os.path.exists(model_path) and os.access(model_path,
                                                                                 os.W_OK) else "data/bigram_freq.pkl"
        self.model = self.load_model()

    def load_model(self):
        """Loads the model if it exists; otherwise, initializes an empty defaultdict."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    return pickle.load(f)
            except Exception as e:
                self.err = True
                self.err_msg = str(e)
                print("Warning: Model file corrupted or missing. Initializing a new model.")
        return defaultdict(Counter)

    def save_model(self):
        """Saves the model to a pickle file."""
        try:
            with open(self.model_path, "wb") as f:
                pickle.dump(self.model, f)
        except Exception as e:
            self.err = True
            self.err_msg = str(e)
            print("Warning: save model issue.")

    def clean_text(self, input_text):
        """Removes URLs, HTML tags, and bracketed words from the text."""
        if not input_text:
            return ""
        # Remove URLs.
        clean_text = rx.remove_url(input_text)
        # Remove HTML tags.
        clean_text = rx.remove_html(clean_text)
        # Remove bracketed words (usually acronyms).
        return rx.remove_bracketed_text(clean_text)

    def convert2sentences(self, clean_text):
        # split the paragraph to sentences
        sentences = sent_tokenize(clean_text)
        # preprocess each sentence before build the model
        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.lower()
            if sentence.strip():
                clean_sentences.append(self.nlp_preprocess(sentence))
        # load all the sentence and update the model
        return clean_sentences

    def nlp_preprocess(self, sentence):
        """Cleans and preprocesses the sentence using NLP preprocessing."""
        if not sentence.strip():
            return ""
        nlp = NLP()
        return nlp.process(sentence)

    def tokenize(self, clean_sentence):
        """Tokenizes a preprocessed sentence."""
        if not clean_sentence:  # Prevents errors on empty strings
            return []
        tokens = word_tokenize(clean_sentence)  # Tokenize sentence
        clean_tokens = []
        contractions = {"s", "re", "m", "ll", "t", "ve"}
        i = 0
        while i < len(tokens):
            if tokens[i] not in contractions:
                clean_tokens.append(tokens[i])
            i += 1
        return clean_tokens

    def update_bigrams(self, input_text):
        try:
            clean_text = self.clean_text(input_text)
            clean_sentences = self.convert2sentences(clean_text)
            for clean_sentence in clean_sentences:
                # split the sentence to tokens
                tokens = self.tokenize(clean_sentence.lower())
                # add on start and end padding in the tokens
                padded_tokens = ["<s>"] + tokens + ["</s>"]
                # generate the bigrams model with nltk
                bigram_list = list(bigrams(padded_tokens))
                # update the new value into existing bigrams model
                for w1, w2 in bigram_list:
                    self.model[w1][w2] += 1
            # save the new bigrams model into physical file
            self.save_model()
            # print(self.load_model())
        except Exception as e:
            self.err = True
            self.err_msg = str(e)
            print("Warning: update bi_grams Issue.")

    def rank_suggestions(self, previous_word, suggestions):
        previous_word = previous_word.lower()
        ranking = {}
        for key in suggestions:
            suggestion = suggestions[key].lower()
            rank = self.model.get(previous_word, {}).get(suggestion, 0)  # Avoid KeyError
            # print(rank)
            if rank not in ranking:
                ranking[rank] = []
            ranking[rank].append(suggestion)
        # Sort by frequency in descending order
        ranked_suggestions = sorted(ranking.items(), key=lambda x: x[0], reverse=True)
        # Flatten sorted suggestions into a dictionary
        my_dict = {}
        i = 0
        for _, words in ranked_suggestions:
            for word in words:
                my_dict[i] = word
                i += 1
        return my_dict

    def check_sentence(self, doc: Document):
        timer = Timer()
        timer.start()

        # is_update = True
        input_text = doc.input_text
        paragraphs = doc.paragraphs

        print(f'[Bigram-Processor:Ranking] - processing {len(paragraphs)} paragraphs...')
        # preprocess the input text without edit distance
        clean_text = self.clean_text(input_text)
        clean_sentences = self.convert2sentences(clean_text)
        i = 0
        j = 0
        for clean_sentence in clean_sentences:
            # split the sentence to tokens
            tokens = self.tokenize(clean_sentence.lower())
            ed_sentences = paragraphs[i].sentences
            ed_tokens = ed_sentences[j].tokens
            previous_token = '<s>'
            for token in tokens:
                for ed_token in ed_tokens:
                    if ed_token.source == token and ed_token.suggestions:
                        ed_token.suggestions = self.rank_suggestions(previous_token, ed_token.suggestions)
                        # is_update = False
                previous_token = token
            j += 1
            if len(ed_sentences) == j:
                i += 1
                j = 0
        # TODO: Removing update safely (not used in NB during building). If not, the model is keep learning wrong context.
        # if is_update:
        # self.update_bigrams(input_text)
        doc.input_text = ''

        print(f'[Bigram-Processor:Ranking] - completed paragraphs in {timer.stop()} seconds.')

    def verify_error_type(self, doc: Document, corpus: PlaintextCorpusReader, stop_words: set[str]):
        input_text = doc.input_text
        paragraphs = doc.paragraphs
        # preprocess the input text without edit distance
        clean_text = self.clean_text(input_text)
        clean_sentences = self.convert2sentences(clean_text)
        i = 0
        j = 0
        for clean_sentence in clean_sentences:
            # split the sentence to tokens
            tokens = self.tokenize(clean_sentence.lower())
            ed_sentences = paragraphs[i].sentences
            ed_tokens = ed_sentences[j].tokens
            previous_token = '<s>'
            for token in tokens:
                for ed_token in ed_tokens:
                    if ed_token.source == token:
                        proba = self.model.get(previous_token, {}).get(ed_token.source, 0)
                        if proba == 0:
                            # TODO: Not sure why stop words are flowing in.
                            if ed_token.source not in stop_words:
                                if ed_token.source in corpus:
                                    ed_token.word_type = WordType.REAL_WORD
                                else:
                                    ed_token.word_type = WordType.NON_WORD

                previous_token = token
            j += 1
            if len(ed_sentences) == j:
                i += 1
                j = 0
