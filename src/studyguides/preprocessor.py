import nltk


class Preprocessor(object):
    def __init__(
            self,
            # A file of stopwords
            stopwords_file=None,
            # Min char length to keep
            min_char_length=2,
            # Use a lemmatizer
            lemmatizer=nltk.WordNetLemmatizer()
    ):
        self.min_char_length = min_char_length
        self.lemmatizer = lemmatizer

        self.stopwords = set()
        if stopwords_file:
            with open(stopwords_file) as f:
                for line in f:
                    self.stopwords.add(line.strip())

    def preprocess(self, document):
        tokens = map(
            lambda token: unicode(token.lower(), 'utf-8'),
            nltk.word_tokenize(document)
        )
        tokens_and_tags = nltk.pos_tag(tokens)
        result_tokens = []

        for token, tag in tokens_and_tags:
            if token in '?.!':
                result_tokens.append(token)
                continue

            if hasattr(self, 'lemmatizer'):
                if tag.startswith('J'):
                    tag = 'a'
                elif tag.startswith('V'):
                    tag = 'v'
                elif tag.startswith('N'):
                    tag = 'n'
                elif tag.startswith('R'):
                    tag = 'r'
                else:
                    tag = 'n'

                token = self.lemmatizer.lemmatize(token, tag)

            if len(token) < self.min_char_length:
                continue

            if token in self.stopwords:
                continue

            if "'" in token:
                continue

            result_tokens.append(token)

        return ' '.join(result_tokens)
