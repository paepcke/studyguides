from collections import Counter, defaultdict
from base_extractor import BaseExtractor

import itertools
import nltk
import warnings
import numpy as np


class CoocurrenceExtractor(BaseExtractor):
    def __init__(
            self,
            # What percentage of terms count as "frequent"?
            frequency_threshold=0.3,
            # Given a list of scores for a word, a fn that combines them into
            # a single word (by default average)
            combination_fn=lambda scores: float(sum(scores)) / len(scores),
            **kwargs
    ):
        super(CoocurrenceExtractor, self).__init__(**kwargs)
        self.frequency_threshold = frequency_threshold
        self.combination_fn = combination_fn

    def extract_documents(self, documents):
        all_scores = defaultdict(list)

        for document in documents:
            for word, score in self.extract_document(document):
                all_scores[word].append(score)

        combined_scores = {
            word: self.combination_fn(scores)
            for word, scores in all_scores.items()
        }

        return sorted(
            combined_scores.items(),
            key=lambda (word, score): score,
            reverse=True
        )

    def extract_document(self, document):
        counts = Counter()
        sents = []

        for sent in nltk.sent_tokenize(document):
            words = self._create_ngrams(nltk.word_tokenize(sent))
            sents.append(words)
            counts.update(words)

        if len(sents) == 1:
            warnings.warn(
                'Only one sentence found. Did you remove punctuation?'
            )

        frequent_words = dict(counts.most_common(
            int(float(len(counts)) * self.frequency_threshold)
        ))

        # this is the map from word => idx
        vocab = {word: idx for idx, word in enumerate(sorted(counts.keys()))}

        # Build an initial cooccurence matrix. This is used for clustering
        cooccurrence_counts = np.zeros((len(vocab), len(vocab)))

        for sent in sents:
            for a, b in itertools.combinations(sent, 2):
                a_idx = vocab[a]
                b_idx = vocab[b]

                cooccurrence_counts[a_idx][b_idx] += 1
                cooccurrence_counts[b_idx][a_idx] += 1

        # This is a map from frequent words to an index
        clusters = {word: idx for idx, word in enumerate(frequent_words)}

        for a, b in itertools.combinations(clusters.keys(), 2):
            a_idx = vocab[a]
            b_idx = vocab[b]

            if self._jensen_shannon_divergence(
                    cooccurrence_counts[:, a_idx],
                    cooccurrence_counts[:, b_idx]
            ) >= 0.95 * np.log(2.0):
                clusters[a] = clusters[b]

        # This is just to remove the gaps from cluster ids.
        normalization_map = {
            unnormalized: idx
            for idx, unnormalized in enumerate(set(clusters.values()))
            }
        clusters = {
            word: normalization_map[unnormalized]
            for word, unnormalized in clusters.items()
            }

        # Now create a coocurrence matrix with clusters. These are freq in the
        # paper.
        cooccurrence_counts = np.zeros(
            (len(vocab), len(set(clusters.values())))
        )

        # These values are the n_w in the paper
        N = np.zeros(len(vocab))

        for sent in sents:
            for a, b in itertools.combinations(sent, 2):
                a_idx = vocab[a]
                b_idx = vocab[b]
                if a in clusters:
                    N[b_idx] += 1
                    cooccurrence_counts[b_idx][clusters[a]] += 1
                if b in clusters:
                    N[a_idx] += 1
                    cooccurrence_counts[a_idx][clusters[b]] += 1

        total_frequent = sum(frequent_words.values())
        # These values are p_g in the paper
        P = np.zeros(len(set(clusters.values())))

        for word, cluster in clusters.items():
            P[cluster] += frequent_words[word]

        P /= total_frequent

        chisq_vals = {}
        for word, word_idx in vocab.items():
            if N[word_idx] == 0: continue
            terms = []
            for frequent_word in frequent_words.keys():
                if word == frequent_word: continue

                frequent_word_idx = clusters[frequent_word]

                observed = cooccurrence_counts[word_idx][frequent_word_idx]
                expected = float(N[word_idx]) * P[frequent_word_idx]

                terms.append((observed - expected)**2 / expected)

            chisq_vals[word] = sum(terms) - max(terms)

        results = chisq_vals.items()
        results = [
            (word, val) for word, val in results
            if len(set('!?.').intersection(set(word))) == 0
            ]

        if self.vocabulary is not None:
            results = filter(
                lambda (word, _val): word in self.vocabulary, results
            )

        return sorted(
            results,
            key=lambda (word, val): val,
            reverse=True
        )

    @staticmethod
    def _jensen_shannon_divergence(dist_a, dist_b):
        dist_a = dist_a.astype(float)
        dist_b = dist_b.astype(float)

        M = (dist_a + dist_b) / 2

        # trim out zeros
        dist_a = np.array([n for idx, n in enumerate(dist_a) if M[idx] != 0])
        dist_b = np.array([n for idx, n in enumerate(dist_b) if M[idx] != 0])
        M = np.array([n for n in M if n != 0])

        # KL for a || M and b || M
        a_M = sum(dist_a * np.log(dist_a / M))
        b_M = sum(dist_b * np.log(dist_b / M))

        return a_M / 2 + b_M / 2