"""
A class for loading word counts [count(w)] from tab-separated-value (TSV) text file to calculate the probability
distribution for a given word.

The text file need to be in the following format, where 'count' is the sum of occurrences of the word in the corpus:
word1<tab>count
word2<tab>count

The probability of P(w) = count(w) / vocab-size (calculated mathematically) can be expressed as:
p = ProbaDistributor(data=<file-path>)
proba = p('apple')

Acknowledgement: The data and code is adopted from Peter Norvig's corpus: https://norvig.com/ngrams/
"""


class ProbaDistributor(dict):
    def __init__(self, data=None, vocab_size=None, missing_handler=None):
        """

        :param data: The corpus file path that contains the word and word counts as described above.
        :param vocab_size: When a corpus is large and was segmented, the count can be assigned manually.
        :param missing_handler: Function to override the default calculation proba for missing word (1 / vocab-size).
        """

        super().__init__()

        if data is None:
            data = []

        # Loads the count(word) values from tab-separated-value file.
        for key, count in data:
            self[key] = self.get(key, 0) + int(count)

        # N is number of tokens in corpus. If N not specified then sum of all the keys' (proba values) assigned.
        # N is the number of tokens in the corpus.
        self.denominator = float(vocab_size or sum(self.values()))

        # The function for handling unknown word (missing in corpus) is defined here.
        # Default probability is 1/N, where N is the number of tokens in the corpus (pg. 224).
        self.missing_handler = missing_handler or (lambda k, d: 1. / d)

    def __call__(self, key):
        if key in self:
            # print(f'P({key}) / {self.denominator}) \t= {float(self[key] / self.denominator)}')
            return self[key] / self.denominator
        else:
            # print(f'P(1 / {self.denominator}) = {1 / self.denominator}')
            return self.missing_handler(key, self.denominator)
