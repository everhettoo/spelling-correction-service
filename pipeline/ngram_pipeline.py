from nlppreprocess import NLP
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
from models.document import Document
from models.paragraph import Paragraph
from models.sentence import Sentence
from models.token import Token
from models.types import WordType
import pickle
import os
import nltk

nltk.download('punkt')  # Ensure NLTK tokenizer is available

class NgramPipeline:
    def __init__(self, n, model_path="data/ngram_model.pkl"):
        self.n = n
        self.model_path = model_path if os.access(model_path, os.W_OK) else "data/default_ngram_model.pkl"
        self.model = self.load_model()

    def load_model(self):
        """Loads the model if it exists; otherwise, initializes an empty defaultdict."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    return pickle.load(f)
            except (FileNotFoundError, pickle.UnpicklingError):
                print("Warning: Model file corrupted or missing. Initializing a new model.")
        return defaultdict(Counter)

    def save_model(self):
        """Saves the model to a pickle file."""
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)

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
        return word_tokenize(clean_sentence)

    def build_model(self, tokens):
        """Builds an n-gram model from a list of tokens."""
        if len(tokens) < self.n:
            print("Warning: Not enough words for an n-gram.")
            return  # Not enough words for an n-gram
        n_grams = list(ngrams(tokens, self.n))
        for n_gram in n_grams:
            prefix, next_word = tuple(n_gram[:-1]), n_gram[-1]
            self.model[prefix][next_word] += 1

    def preprocess_build_model(self, sentence: str):
        """Processes input sentence and updates the n-gram model."""
        clean_sentence = self.nlp_preprocess(sentence)
        tokens = self.tokenize(clean_sentence)
        self.build_model(tokens)
        self.save_model()  # Save after updating the model
        self.print_model()  # Print the updated model for debugging

    def predict_next(self, context):
        context = tuple(context[-(self.n - 1):])  # Keep only relevant context
        if context in self.model:
            return self.model[context].most_common(1)[0][0]  # Most probable next word
        else:
            return None  # No prediction

    def check_sentence(self, doc: Document):
        """Checks if a sentence follows the trained n-gram model using structured input."""

        # Extract input text and tokens from structured input
        input_text = doc.input_text
        paragraphs = doc.paragraphs

        tokens = []
        for paragraph in paragraphs:
            for sentence in paragraph.sentences:
                for token in sentence.tokens:
                    if token.word_type != 4:
                        tokens.extend([token.source])

        if len(tokens) < self.n:
            return {
                "doc": doc,
                "message": "Sentence is too short for this n-gram model.",
            }

        context = ['']
        for token in tokens:
            context.extend(token)
            if len(context) > 2:
                context.pop(0)
            predicted_word = self.predict_next(context)
            if predicted_word:
                print(predicted_word)
                token.suggestions[len(list(token.suggestions.keys()))+1] = predicted_word

        return {
            "doc": doc,  # Return original structure
            "message": "Sentence consistency checked.",
        }


    def print_model(self):
        """Prints the n-gram model in a readable format."""
        print("\n=== N-Gram Model ===")
        print(self.n)
        if not self.model:
            print("Model is empty.")
        for prefix, next_words in self.model.items():
            formatted_prefix = " ".join(prefix) if isinstance(prefix, tuple) else prefix
            print(f"{formatted_prefix} -> {dict(next_words)}")
        print("====================\n")
