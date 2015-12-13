import os

def get_documents(directory, stopwords):
  captionDocuments = dict()
  videoDocuments = dict()
  for root, directories, _ in os.walk(directory):
    for directory in directories:
      filename = root + directory + "/both_cleaned.txt"
      with open(filename) as f:
        time = f.readline().strip()
        while time != "":
          event = f.readline().strip()
          slideText = ' '.join([token for token in f.readline().strip().lower().split(" ") \
            if token not in stopwords])
          captionText = ' '.join([token for token in f.readline().strip().lower().split(" ") \
            if token not in stopwords])
          f.readline()
          if event == "slide":
            videoDocuments[directory + "-" + time] = slideText
            captionDocuments[directory + "-" + time] = captionText
          time  = f.readline().strip()
  keys = videoDocuments.keys()
  for key in keys:
    if videoDocuments[key] == "":
      del videoDocuments[key]
  keys = captionDocuments.keys()
  for key in keys:
    if captionDocuments[key] == "":
      del captionDocuments[key]
  return (captionDocuments, videoDocuments)

def get_stopwords():
  stopwords = list()
  with open('../indexing/gen_indeces/long-stopwords.txt') as f:
    stopwords += [line.strip().replace("'", "") for line in f]
  with open('../indexing/gen_indeces/extra-stopwords.txt') as f:
    stopwords += [line.strip().replace("'", "") for line in f]
  with open('../indexing/gen_indeces/remove-stopwords.txt') as f:
    for line in f:
      line = line.strip().replace("'", "")
      if line in stopwords:
        stopwords.remove(line)
  return stopwords

stopwords = get_stopwords()
captionDocuments, videoDocuments = get_documents("../../data/video_frames/", stopwords)

def get_occurences(one, two):
  vidcount = 0
  keywords = one.split("_") + two.split("_")
  for key in videoDocuments:
    value = videoDocuments[key]
    contains = True
    for keyword in keywords:
      if keyword not in value:
        contains = False
        break
    if contains:
      vidcount += 1
  capcount = 0
  for key in captionDocuments:
    value = captionDocuments[key]
    contains = True
    for keyword in keywords:
      if keyword not in value:
        contains = False
        break
    if contains:
      capcount += 1
  return (vidcount, capcount)
