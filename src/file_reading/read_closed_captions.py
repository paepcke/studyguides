import re
import os
from collections import Counter
from sets import Set

HOME_PATH = "/afs/.ir.stanford.edu/users/j/o/josehdz/"
SW_REL_PATH = "studyguides/data/nlp/english_stopwords_long"
CC_REL_PATH = "studyguides/data/closed_captions/"
CC_REL_DIRS = ["stanford-online-ee364/"]

CC_DIGITS_REGEX = "\d+"
CC_SEC_PER_INTERVAL = 300

stopwords = Set()

def init_stopwords_set():
  with open(HOME_PATH + SW_REL_PATH) as f:
    for line in f:
      stopwords.add(line.strip())

def prune_stopwords_from_dict(dictionary):
  for stopword in stopwords:
    dictionary.pop(stopword, None)
  return dictionary

# [hrs, min, sec] => total seconds
def hms_to_seconds(time):
  seconds_ratio = 1
  seconds = 0
  for i in reversed(range(0, len(time))):
    seconds += seconds_ratio * int(time[i])
    seconds_ratio *= 60
  return seconds

# returns dictionary with relevant information
def read_lines_in_file(filename):
  print "read_closed_captions.py: processing filename = ", filename
  fileIntervalFreqs = list() # [[line, time], [line, time], ... ]
  fileFreqs = Counter()
  with open(filename) as f:
    timestamp = 0
    prevTimestamp = 0
    intervalFreqs = Counter()
    for line in f:
      if line and line[0].isalpha(): 
        # handles case for text lines
        freqs = Counter([token.lower().strip() for token in line.split(' ')])
        fileFreqs += freqs
        intervalFreqs += freqs
####      else:
####        matches = re.findall(CC_DIGITS_REGEX, line)
####        if 3 <= len(matches):
####          # this is the start time for the phrase
####          # matches [hrs, min, sec]
####          timestamp = hms_to_seconds(matches[0:3])
####          if (prevTimestamp + CC_SEC_PER_INTERVAL) <= timestamp:
####            # start a new bucket
####            prune_stopwords_from_dict(intervalFreqs)
####            fileIntervalFreqs.append([prevTimestamp, intervalFreqs])
####            intervalFreqs = Counter()
####            prevTimestamp += CC_SEC_PER_INTERVAL

    # pick up leftover bucket
    if timestamp < (prevTimestamp + CC_SEC_PER_INTERVAL):
      prune_stopwords_from_dict(intervalFreqs)
      fileIntervalFreqs.append([prevTimestamp, intervalFreqs])

  prune_stopwords_from_dict(fileFreqs)
  return {'interval_freqs': fileIntervalFreqs, 'freqs': fileFreqs, 'interval': CC_SEC_PER_INTERVAL}

def read_files_in_dir(directory):
  print "read_closed_captions.py: processing directory = ", directory
  dirData = dict()
  for filename in os.listdir(directory):
    dirData[filename] = read_lines_in_file(directory + filename)
    print dirData[filename]['interval']
    print len(dirData[filename]['interval_freqs'])
    print dirData[filename]['interval_freqs']
    print dirData[filename]['freqs']
  return dirData

init_stopwords_set() 
for directory in CC_REL_DIRS:
  directory = HOME_PATH + CC_REL_PATH + directory
  dirData = read_files_in_dir(directory)
