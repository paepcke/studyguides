import os.path
import datetime
import nltk

import numpy as np
#import matplotlib.pyplot as plt

from pprint import pprint
from collections import OrderedDict, Counter
from sklearn.feature_extraction.text import TfidfVectorizer

def get_documents(directory, stopwords):
  documents = dict()
  for root, directories, _ in os.walk(directory):
    for directory in directories:
      filename = root + directory + "/unique_slide_info.txt"
      with open(filename) as f:
        time = f.readline().strip()
        while time != "":
          event = f.readline().strip()
          text  = [token for token in f.readline().strip().split(" ") \
            if token not in stopwords]
          f.readline()
          if event == "slide":
            documents[directory + "-" + time] = text
          time  = f.readline().strip()
  keys = documents.keys()
  for key in keys:
    if documents[key] == "":
      del documents[key]
  return documents

def get_stopwords():
  stopwords = list()
  with open('long-stopwords.txt') as f:
    stopwords += [line.strip().replace("'", "") for line in f]
  with open('extra-stopwords.txt') as f:
    stopwords += [line.strip().replace("'", "") for line in f]
  with open('remove-stopwords.txt') as f:
    for line in f:
      line = line.strip().replace("'", "")
      if line in stopwords:
        stopwords.remove(line)
  return stopwords

def get_pos_tokens(documents):
  sentences = [nltk.word_tokenize(sent) \
    for sent in nltk.sent_tokenize(' '.join(documents.values()))]
  tags = []
  for sentence in sentences:
    try:
      tags.append(nltk.pos_tag(sent))
    except UnicodeDecodeError:
      print "error: ", sentence
      pass
  pos_to_tokens = {}
  for sent in tags:
    for token, pos in sent:
      if pos not in pos_to_tokens:
          pos_to_tokens[pos] = set([token.lower()])
      else:
          pos_to_tokens[pos].add(token.lower())
  return pos_to_tokens

def get_lemmatized_docs(documents, stop_words):
  lemmatizer = nltk.WordNetLemmatizer()
  lemmatized_docs = OrderedDict()
  for key, doc in documents.items():
    tokens = nltk.word_tokenize(doc)
    lemmatized_tokens = []
    for token in tokens:
      if token not in stop_words:
        try:
          lemmatized_tokens.append(lemmatizer.lemmatize(token))
        except:
          pass          
    lemmatized_docs[key] = ' '.join(lemmatized_tokens) 
  return lemmatized_docs

def get_vocabulary(tfidf):
  filtered_vocabulary = dict()
  for key, value in tfidf.vocabulary_.items():
    if Counter(key.split()).most_common()[0][1] == 1 and \
        not any([key in other and key != other for other in filtered_vocabulary]):
      filtered_vocabulary[key] = value

  return filtered_vocabulary

def get_filtered_vocabulary(pos_to_tokens, tfidf):
  VALID_TAGS = [
    'NNP',
    'NNPS',
  ]
  valid_tokens = set()
  for pos in VALID_TAGS:
    if pos in pos_to_tokens:
      valid_tokens = valid_tokens.union(pos_to_tokens[pos])
    else:
      print "josehdz: key not found: ", pos

  filtered_vocabulary = dict()
  for key, value in tfidf.vocabulary_.items():
    if len(set(key.split()).intersection(valid_tokens)) > 0 and \
        Counter(key.split()).most_common()[0][1] == 1 and \
        not any([key in other and key != other for other in filtered_vocabulary]):
      filtered_vocabulary[key] = value

  return filtered_vocabulary

#stopwords = get_stopwords()
#documents = get_documents("../../data/video_frames/", stopwords)
# ## print "processing pos_to_tokens"
# ## pos_to_tokens = get_pos_tokens(documents)
# ## print "processing lemmatized_docs"
# ## lemmatized_docs = get_lemmatized_docs(documents, stopwords)
# ## 
#tfidf = TfidfVectorizer(
#    stop_words=stopwords,
#    ngram_range=(1,4),
#    max_features=1000,
#    max_df=30
#)
#X = tfidf.fit_transform(documents.values())
# ## X = tfidf.fit_transform(lemmatized_docs.values())
#print "processing vocabulary"
# ## vocabulary = get_filtered_vocabulary(pos_to_tokens, tfidf)
#vocabulary = get_vocabulary(tfidf)
#pprint(vocabulary
