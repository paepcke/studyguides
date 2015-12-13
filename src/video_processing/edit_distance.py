import argparse
import constants
import editdistance
import os
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument('--regen-vocab', action='store_true', dest='regen_vocab', default=False)
parser.add_argument('--window', action="store", dest="window", default=3)
args = parser.parse_args()
args.window = int(args.window)
print "window = ", args.window, type(args.window)

vocabulary = dict()
captionKeywords = list()

def initializeVocabulary(vocabfile):
  global vocabulary
  with open(vocabfile) as f:
    for line in f:
      indexterm = line.strip().lower()
      for word in indexterm.split(" "):
        lastStart = len(word) - args.window
        for start in range(lastStart + 1):
          window = word[start:(start + args.window)]
          assert len(window) == args.window
          vocabulary[window] = vocabulary.get(window, list()) + [word]
 
def getSpelling(word):
  minDistance = float('+inf')
  spellings = dict()
  lastStart = len(word) - args.window
  for start in range(lastStart + 1):
    window = word[start:(start + args.window)]
    assert len(window) == args.window
    for candidate in vocabulary.get(window, list()):
      distance = editdistance.eval(word, candidate)
      if distance <= minDistance and \
          candidate not in spellings.get(distance, list()):
        minDistance = distance
        spellings[distance] = spellings.get(distance, list()) + [candidate]
  preferred = list()
  leftover = list()
  if minDistance == float('+inf'):
    return ""
  for spelling in spellings[minDistance]:
    if spelling in captionKeywords:
      preferred.append(spelling)
    else:
      leftover.append(spelling)
  return random.choice(preferred) if 0 < len(preferred) else random.choice(leftover)

def createVocabFile():
  seen = set()
  for (dirpath, dirnames, filenames) in os.walk(constants.CAPTIONS_REL_PATH):
    print "dirpath: ", dirpath
    for f in filenames:
      filename = dirpath + f
      print "filename: ", filename
      with open (filename) as src:
        for line in src:
          line = line.strip().lower()
          line = line.replace("&#39;", " '")
          line = ''.join([ch for ch in line if (ch.isalnum() or ch.isspace())])
          words = line.lower().split(" ")
          for word in words:
            if not word.isdigit():
              seen.add(word)
  os.system("rm -f gold-vocabulary.txt")
  with open("gold-vocabulary.txt", "w+") as tgt:
    for word in seen:
      tgt.write(word + "\n")

if args.regen_vocab:
  createVocabFile()
initializeVocabulary("gold-vocabulary.txt")
