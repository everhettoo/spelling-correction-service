# This module contains all the types used in the application.
from enum import Enum


class WordType(Enum):
    # The word types are defined here:
    UNDEFINED = -1
    WORD = 1
    NON_WORD = 2
    PUNCTUATION = 3
    STOP_WORD = 4
    APOSTROPHE = 5
    CONTRACTION = 6
    REAL_WORD = 7
