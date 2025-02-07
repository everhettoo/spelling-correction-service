# This module handles:
# 1. language encoding and language detection
# 2. word tokenization (word segmentation)

from nltk.tokenize import word_tokenize
import chardet


def detect_language_when_english(text):
    # TODO: To implement the logic.
    input_text = text.encode()
    result = chardet.detect(input_text)['encoding']
    if result == 'ascii':
        return True
    else:
        return False


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
