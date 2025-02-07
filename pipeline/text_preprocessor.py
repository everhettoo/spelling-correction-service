# This module handles:
# 1. language encoding and language detection
# 2. word tokenization (word segmentation)

from nltk.tokenize import word_tokenize


def tokenize_words(text: str):
    """
    This method tokenizes the text and returns tokens when no error occurs.
    :param: the input string.
    :return: list of strings as tokens.
    """
    try:
        tokens = word_tokenize(text)
        # TODO: Need more careful handling where lib misses few words like bart's. Custom expression??

        return tokens
    except Exception as e:
        raise e
