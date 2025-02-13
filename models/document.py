from typing import List

from nltk.tokenize import sent_tokenize, word_tokenize

from models.sentence import Sentence
from models.paragraph import Paragraph
from models.token import Token


class Document:

    def __init__(self, input_text: str):
        self.input_text = input_text
        self.paragraphs: List[Paragraph] = []

    # def parse_doc(self):
    #     self.paragraphs = []
    #     paragraph_list = self.input_text.split("\r\n")
    #     for p in paragraph_list:
    #         # Process paragraph
    #         paragraph = Paragraph()
    #         sentence_list = sent_tokenize(p)
    #         for s in sentence_list:
    #             # Process sentence
    #             sentence = Sentence()
    #             words = word_tokenize(s)
    #             for word in words:
    #                 # Process token
    #                 sentence.tokens.append(Token(word))
    #
    #             # Add processed sentence (+tokens) into a new paragraph.
    #             paragraph.sentences.append(sentence)
    #
    #         # Add the new paragraph into document.
    #         self.paragraphs.append(paragraph)

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
