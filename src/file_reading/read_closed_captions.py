import re
import os
from collections import Counter

HOME_PATH = "/afs/.ir.stanford.edu/users/j/o/josehdz/"
CC_DIGITS_REGEX = "\d+"
CC_REL_PATH = "studyguides/data/closed_captions/"
CC_REL_DIRS = ["CompilersSelfPacedCS1/", "stanford-online-ee364/"]

def cat_integers(integers):
  s = ""
  for i in integers:
    s += str(i)
  return int(s)

def read_lines_in_file(filename):
  print "read_closed_captions.py: read_lines_in_file: processing filename = ", filename
  captions = list() # [[line, time], [line, time], ... ]
  freqs = Counter()
  with open(filename) as f:
    timestamp = -1
    for line in f:
      if line and line[0].isalpha(): 
        # handles case for text lines
        captions.append([line, timestamp])
        freqs += Counter(line.split(" "))
      else:
        matches = re.findall(CC_DIGITS_REGEX, line)
        if 3 <= len(matches):
          # this is the start time for the phrase
          # [hrs, min, sec]
          timestamp = cat_integers(matches[0:3])
  return {'captions': captions, 'frequencies': freqs}

def read_files_in_dir(directory):
  print "read_closed_captions.py: read_files_in_dir: processing directory = ", directory
  dirData = dict()
  for filename in os.listdir(directory):
    dirData[filename] = read_lines_in_file(directory + filename)
  return dirData

for directory in CC_REL_DIRS:
  directory = HOME_PATH + CC_REL_PATH + directory
  dirData = read_files_in_dir(directory)
