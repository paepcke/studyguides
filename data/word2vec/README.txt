============================================================
file: prune-vectors.py

This script prunes the word vectors based on the index terms.
The pruned set of vectors should only contain the vectors 
needed to represent the terms in our index and nothing more.

Flags:

--index <filename> :
  name of the file that contains the words that we should
  keep from the total list of words

--ngrams :
  Specifies that we should keep the word vectors for every
  word in the indexfile. This means that if "first set" is
  an index term, then we will save the word vectors for
  "first" and "set". By default, this value is False and will
  ignore the constituents of "first set" and only save the
  vectors for unigram index terms.

--source <dirname> :
  the folder that contains the file named word-vectors.bin 
  and word-vocab.txt which will be read but not modified. 
  This is also where the new pruned vector files will go.

--verbose:
  prints things
