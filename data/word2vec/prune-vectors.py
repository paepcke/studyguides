import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--index', action='store', dest='indexfile', default="")
parser.add_argument('--source', action="store", dest="sourcedir", default="")
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False)
parser.add_argument('--ngrams', action='store_true', dest='ngrams', default=False)
args = parser.parse_args()

def getVocabulary():
  vocab = list()
  src = open(args.indexfile)
  for line in src:
    if args.ngrams:
      tokens = line.strip().lower().split(" ")
      for token in tokens:
        if token not in vocab:
          vocab.append(token)
    else:
      line = line.strip()
      line = '_'.join(line.split(" "))
      if line not in vocab:
        vocab.append(line)
  src.close()
  return vocab

def pruneWordVectors(vocabulary):
  vectorSrc = open(args.sourcedir + "word-vectors.bin", "r")
  vocabSrc = open(args.sourcedir + "word-vocab.txt", "r")
  os.system("rm -f " + args.sourcedir + "word-vectors-pruned.bin")
  os.system("rm -f " + args.sourcedir + "word-vocab-pruned.txt")
  vectorTgt = open(args.sourcedir + "word-vectors-temp.bin", "w+")
  vocabTgt = open(args.sourcedir + "word-vocab-pruned.txt", "w+")

  vectorTgt.write(vectorSrc.readline()) # metadata
  word = vocabSrc.readline().strip()
  tokens = word.split(" ")
  word = ''.join(tokens[0 : (len(tokens) - 1)])
  nextWord = vocabSrc.readline().strip()
  tokens = nextWord.split(" ")
  nextWord = ''.join(tokens[0 : (len(tokens) - 1)])

  vector = vectorSrc.readline() 
  while len(word) > 0:
    keepVector = word in vocabulary
    if keepVector:
      vocabTgt.write(word + "\n")
    while nextWord != vector and not vector.startswith(nextWord):
      # handles case when both reach EOF
      # handles case when reach next vector
      if keepVector:
        vectorTgt.write(vector)
      vector = vectorSrc.readline()
    word = nextWord
    nextWord = vocabSrc.readline().strip()
    tokens = nextWord.split(" ")
    nextWord = ''.join(tokens[0 : (len(tokens) - 1)])
    
  vectorSrc.close()
  vocabSrc.close()
  vectorTgt.close()
  vocabTgt.close()    

  # clean up metadata
  vocabSrc = open(args.sourcedir + "word-vocab-pruned.txt", "r")
  count = 0
  for line in vocabSrc:
    count += 1
  vocabSrc.close()

  vectorSrc = open(args.sourcedir + "word-vectors-temp.bin", "r")
  vectorTgt = open(args.sourcedir + "word-vectors-pruned.bin", "w+")
  tokens = vectorSrc.readline().strip().split(" ")
  vectorTgt.write(str(count) + " " + tokens[1] + "\n")
  for line in vectorSrc:
    vectorTgt.write(line)
  vectorSrc.close()
  vectorTgt.close()
  os.system("rm -f "+ args.sourcedir + "word-vectors-temp.bin")

def prunePhraseVectors(vocabulary):
  vectorSrc = open(args.sourcedir + "phrases-vectors.bin", "r")
  vocabSrc = open(args.sourcedir + "phrases-vocab.txt", "r")
  os.system("rm -f " + args.sourcedir + "phrases-vectors-pruned.bin")
  os.system("rm -f " + args.sourcedir + "phrases-vocab-pruned.txt")
  vectorTgt = open(args.sourcedir + "phrases-vectors-temp.bin", "w+")
  vocabTgt = open(args.sourcedir + "phrases-vocab-pruned.txt", "w+")

  vectorTgt.write(vectorSrc.readline()) # metadata
  word = vocabSrc.readline().strip()
  tokens = word.split(" ")
  word = ''.join(tokens[0 : (len(tokens) - 1)])
  nextWord = vocabSrc.readline().strip()
  tokens = nextWord.split(" ")
  nextWord = ''.join(tokens[0 : (len(tokens) - 1)])

  vector = vectorSrc.readline() 
  while len(word) > 0:
    keepVector = word in vocabulary
    if keepVector:
      vocabTgt.write(word + "\n")
    while nextWord != vector and not vector.startswith(nextWord):
      # handles case when both reach EOF
      # handles case when reach next vector
      if keepVector:
        vectorTgt.write(vector)
      vector = vectorSrc.readline()
    word = nextWord
    nextWord = vocabSrc.readline().strip()
    tokens = nextWord.split(" ")
    nextWord = ''.join(tokens[0 : (len(tokens) - 1)])
    
  vectorSrc.close()
  vocabSrc.close()
  vectorTgt.close()
  vocabTgt.close()    

  # clean up metadata
  vocabSrc = open(args.sourcedir + "phrases-vocab-pruned.txt", "r")
  count = 0
  for line in vocabSrc:
    count += 1
  vocabSrc.close()

  vectorSrc = open(args.sourcedir + "phrases-vectors-temp.bin", "r")
  vectorTgt = open(args.sourcedir + "phrases-vectors-pruned.bin", "w+")
  tokens = vectorSrc.readline().strip().split(" ")
  vectorTgt.write(str(count) + " " + tokens[1] + "\n")
  for line in vectorSrc:
    vectorTgt.write(line)
  vectorSrc.close()
  vectorTgt.close()
  os.system("rm -f "+ args.sourcedir + "phrases-vectors-temp.bin")

vocabulary = getVocabulary()
pruneWordVectors(vocabulary)
prunePhraseVectors(vocabulary)
