import nltk
from collections import Counter, defaultdict
from base_extractor import BaseExtractor
import numpy as np


class TfidfExtractor(BaseExtractor):
    def __init__(
            self,
            **kwargs
    ):
        super(TfidfExtractor, self).__init__(**kwargs)

    def extract_documents(self, documents):
        self._tfs = Counter()
        self._dfs = Counter()

        for i, document in enumerate(documents):
            words = filter(
                lambda phrase: len(set('.?!').intersection(set(phrase))) == 0,
                self._create_ngrams(nltk.word_tokenize(document))
            )
            self._tfs.update(Counter(words))
            self._dfs.update({word: 1 for word in words})

        n_samples = len(documents) + 1
        self._dfs.update({word: 1 for word in self._dfs.keys()})

        self._idfs = {
            word: np.log(float(n_samples) / self._dfs[word]) + 1
            for word in self._dfs.keys()
        }

        results = [
            (word, self._tfs[word] * self._idfs[word])
            for word in self._tfs.keys()
            ]

        if self.vocabulary is not None:
            results = filter(
                lambda (word, _score): word in self.vocabulary, results
            )

        return sorted(
            results,
            key=lambda (word, val): val,
            reverse=True
        )
