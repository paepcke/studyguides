import nltk

class BaseExtractor(object):

    def __init__(
            self,
            # The end is exclusive
            ngram_range=range(1, 2),
            # Specify a vocabulary.
            vocabulary=None
    ):
        self.ngram_range = ngram_range
        self.vocabulary = vocabulary

    def _create_ngrams(self, tokens):
        results = []
        for n in self.ngram_range:
            for i in range(0, len(tokens) - (n - 1)):
                results.append(' '.join(tokens[i:i + n]))
        return results


