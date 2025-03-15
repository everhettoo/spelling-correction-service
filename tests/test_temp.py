from unittest import TestCase
import nltk
import spacy
from textblob import TextBlob


text1 = "I can't sing'"
text2 = "that is jack's cat'"



class Test(TestCase):
    def test_nltk(self):
        tokens = nltk.tokenize.word_tokenize(text1)
        print("tokens:", tokens)
    def test_spacy(self):
        # nlp = spacy.load("en_core_web_sm")
        # nlp.add_pipe("merge_entities")
        # doc = nlp(text1)
        # for d in doc:
        #     print(d.text)
        nlp = spacy.load('en_core_web_sm')
        nlp.tokenizer.rules = {key: value for key, value in nlp.tokenizer.rules.items() if
                               "'" not in key and "’" not in key and "‘" not in key}
        assert [t.text for t in nlp("can't")] == ["can't"]
        doc = nlp(text2)
        for d in doc:
            print(d.text)

    def test_tb(self):
        tokens = TextBlob(text1).tokens
        print("tokens:", tokens)


        # for ent in doc.ents:
        #     ent(tag=ent.root.tag_, lemma=ent.text, ent_type=ent.label_)
        # print("tokens:", doc)



