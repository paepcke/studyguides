import constants
import edit_distance as ed
import os, os.path
import re
import string
import sys

CC_DIGITS_REGEX = "\d+"

trantab = string.maketrans(string.punctuation, ''.join([" " for _ in string.punctuation]))

# [hrs, min, sec, millisec] => total seconds
def hms_to_seconds(line):
  time = re.findall(CC_DIGITS_REGEX, line)
  if len(time) < 3:
    return -1
  seconds_ratio = 1
  seconds = 0
  for i in reversed(range(3)):
    seconds += seconds_ratio * int(time[i])
    seconds_ratio *= 60
  if 4 <= len(time):
    seconds = float(seconds) + 0.001 * float(time[3])
  return seconds

def get_lecture_name(directory):
  paths = directory.split('/')
  tokens = paths[len(paths) - 2].split('-')
  if tokens[0] == "EDIT":
    name = '-'.join(tokens[2:])
    #print "josehdz: ", name
    return (name, float(tokens[1]))
  else:
    name = '-'.join(tokens)
    #print "josehdz: ", name
    return (name, float(0))

def create_clean_merge(lecturedir):
  # File follows structure:
  ##  1) caption time
  ##  2) event
  ##  3) slide text
  ##  4) caption text
  ##  5) blank line
  with open(lecturedir + "both.txt") as src:
    with open(lecturedir + "both_cleaned.txt", "w+") as tgt:
      time = src.readline().strip()
      while 0 < len(time):
        event = src.readline().strip()
        slideText = src.readline().strip()
        captionText = src.readline().strip()
        src.readline().strip() # blank line

        slideTokens = slideText.split(" ")
        for i in range(len(slideTokens)):
          slideTokens[i] = ed.getSpelling(slideTokens[i])
        slideText = ' '.join(slideTokens)        
        tgt.write(time + "\n")
        tgt.write(event + "\n")
        tgt.write(slideText + "\n")
        tgt.write(captionText + "\n")
        tgt.write("\n")

        time = src.readline().strip()

def process_captions(lecturedir):
  lecture, offset = get_lecture_name(lecturedir)
  captionfile = constants.CAPTIONS_REL_PATH + lecture + ".srt"
  framefile = lecturedir + "unique_slide_info.txt"
  bothfile = lecturedir + "both.txt"
##  bothfileCopy = lecturedir + lecture + ".txt"
  os.system("rm -f " + bothfile) ## + " " + bothfileCopy)
##  print "josehdz: lecture: ", lecture
##  print "josehdz: offset:  ", offset
##  print "josehdz: bothfile: ", bothfile
##  print "josehdz: framefile: ", framefile

  try:
    f = open(framefile)
    f.close()
    f2 = open(captionfile)
    f.close()
    f3 = open(bothfile, 'w+')
    f.close()
  except:
    print "     exception!"
    print "          framefile:", framefile
    print "          captionfile:", captionfile
    return None

##  cpy = open(bothfileCopy, "w+")
  with open(framefile) as infosrc:
    with open(captionfile) as captsrc:
      with open(bothfile, 'w+') as tgt:
        infoTime = hms_to_seconds(infosrc.readline()) # trash the first timestamp

        captionIndex = captsrc.readline().strip()
        captionTime = hms_to_seconds(captsrc.readline())
        prevCaptionTime = captionTime
        captionText = ''

        while infoTime < float('+inf'):
          infoEvent = infosrc.readline().strip()
          infoText = infosrc.readline().strip()
          infosrc.readline() # blank line
          infoTime = infosrc.readline().strip()
          if infoTime == '':
            infoTime = float('+inf')
          else:        
            infoTime = float(hms_to_seconds(infoTime)) + offset
            

          while captionIndex != '' and captionTime < infoTime:
            captionText += (captsrc.readline().strip() + " ")
            captsrc.readline()
            captionIndex = captsrc.readline().strip()
            captionTime = hms_to_seconds(captsrc.readline().strip())
          captionText = captionText.replace("&#39;", " '")
          captionText = ''.join([ch for ch in captionText if (ch.isalnum() or ch.isspace())])

          tgt.write(str(prevCaptionTime) + '\n')
          tgt.write(infoEvent + '\n')
          tgt.write(infoText.lower() + '\n')
          tgt.write(captionText.lower() + '\n')
          tgt.write('\n')

##          cpy.write(str(prevCaptionTime) + '\n')
##          cpy.write(infoEvent + '\n')
##          cpy.write(infoText + '\n')
##          cpy.write(captionText + '\n')
##          cpy.write('\n')

          captionText = ''
          prevCaptionTime = captionTime
##  cpy.close()
  create_clean_merge(lecturedir) 
          

parentDir = constants.FRAME_REL_PATH
ncompleted = 0
for directory in os.listdir(parentDir):
  if not directory[0] == '.' and not directory[0] == '..':
#    #print "processing directory ", directory
    ncompleted += 1
    if ncompleted <= float('+inf'):
      process_captions(parentDir + directory + '/')
