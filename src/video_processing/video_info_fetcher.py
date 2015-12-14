import argparse
import constants
import editdistance
import os, os.path
import PIL
import pytesseract
import string

MIN_WRITING_FRAMES = 6

SLIDE_DREG_MIN = 0.75 * constants.REGION_ROWS * constants.REGION_COLS
SLIDE_DP_MIN = 100000
WRITE_DREG_MIN = 1
WRITE_DP_MIN = 3000 # number of pixels

parser = argparse.ArgumentParser()
parser.add_argument('--rerun-ocr', action='store_true', dest='rerun_ocr', default=False);
parser.add_argument('--rerun-labels', action='store_true', dest='rerun_labels', default=False);
parser.add_argument('--continue-after', action="store", dest="continue_after", default="dummy")
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False);
args = parser.parse_args()

def get_frame_info(framepath):
  basename = os.path.basename(framepath).split(constants.IMG_EXT)[0]
  tokens = basename.split('_')
  last = len(tokens) - 1
  return (tokens[1], int(tokens[2]), int(tokens[3]))

def is_new_slide(dpix, dreg, text, prevText):
  dist = editdistance.eval(text, prevText)
  ratio = float(dist) / float(len(prevText))
  return SLIDE_DP_MIN <= dpix and SLIDE_DREG_MIN <= dreg and 0.5 <= ratio

def is_writing_frame(dpix, dreg):
  return WRITE_DP_MIN <= dpix and WRITE_DREG_MIN <= dreg

def get_framedir_info(framedir):
  tokens = framedir.split('-')
  if tokens[0] == 'EDIT':
    return (float(tokens[1]), '-'.join(tokens[2:]))
  else:
    return (0, framedir)

def extract_text_info(framedir):
  os.system('find ' + framedir + ' -empty -type f -delete')
  frameInfoFilename = framedir + "slide_text.txt"
  rawFrameInfoFilename = framedir + "raw_slide_text.txt"
  os.system("rm -f " + frameInfoFilename + " " + rawFrameInfoFilename)
  trantab = string.maketrans(string.punctuation, ''.join([" " for _ in string.punctuation]))
  fraw = open(rawFrameInfoFilename, "w")
  with open(frameInfoFilename, "w") as fout:
    numConsecWritingFrames = 0
    detectedWriting = False
    detectedWritingTime = ""
    for root, _, files in os.walk(framedir):
      lastFrameType = None
      for f in files:
        if f.endswith(constants.IMG_EXT):
          time, dpix, dreg = get_frame_info(f)
          image = PIL.Image.open(framedir + f)
          slideText = pytesseract.image_to_string(image)
          fraw.write(str(time) + '\n')
          fraw.write(str(dpix) + '\n')
          fraw.write(str(dreg) + '\n')
          fraw.write(slideText + '\n')
          slideText = slideText.replace("\n", " ")
          slideText = slideText.translate(trantab)
          slideText = ' '.join([tok.strip() for tok in slideText.split(" ") if tok.isalnum()])
          fout.write(str(time) + '\n')
          fout.write(str(dpix) + '\n')
          fout.write(str(dreg) + '\n')
          fout.write(slideText + '\n')

  fraw.close() 

def extract_event_info(framedir):
  textInfoFilename = framedir + "slide_text.txt"
  frameInfoFilename = framedir + "unique_slide_info.txt"
  os.system("rm -f " + frameInfoFilename)
  with open(frameInfoFilename, "w") as fout:
    with open(textInfoFilename) as src:
      numConsecWritingFrames = 0
      detectedWriting = False
      detectedWritingTime = ""
      prevText = "e" # dummy string

      while True:
        time = src.readline().strip()
        if time == "": break
        dpix = int(src.readline().strip()) 
        dreg = int(src.readline().strip())
        text = src.readline().strip() 

        if is_new_slide(dpix, dreg, text, prevText):
          fout.write(time + '\n')
          fout.write("slide\n")
          fout.write(text + '\n')
          fout.write("\n")
          numConsecWritingFrames = 0
          detectedWriting = False
          detectedWritingTime = ""
          prevText = text if text != "" else "e"
  
        elif is_writing_frame(dpix, dreg):
          # indicates minor changes in screen
          numConsecWritingFrames += 1
          if len(detectedWritingTime) == 0:
            detectedWritingTime = time
          if MIN_WRITING_FRAMES <= numConsecWritingFrames \
              and not detectedWriting:
            fout.write(detectedWritingTime + '\n')
            fout.write("writing\n")
            fout.write("\n")
            fout.write("\n")
            detectedWriting = True

parentDir = constants.FRAME_REL_PATH
shouldProcess = (args.continue_after == "")
for directory in os.listdir(parentDir):
  if not directory[0] == '.' and shouldProcess:
    if args.verbose:
      print "processing directory ", directory
      print get_framedir_info(directory)
    if args.rerun_ocr:
      extract_text_info(parentDir + directory + '/')
    if args.rerun_labels:
      extract_event_info(parentDir + directory + '/')
  elif directory == args.continue_after:
    shouldProcess = True

##    numConsecWritingFrames = 0
##    detectedWriting = False
##    detectedWritingTime = ""
##    for root, _, files in os.walk(framedir):
##      lastFrameType = None
##      for f in files:
##        if f.endswith(constants.IMG_EXT):
##          time, dpix, dreg = get_frame_info(f)
##          if is_slide_frame(dpix, dreg):
##            # TODO: eventually, write slide text here
##            #       using python tesseract library
##            image = PIL.Image.open(framedir + f)
##            slideText = pytesseract.image_to_string(image)
##            slideText = slideText.replace("\n", " ")
##            slideText = slideText.translate(trantab)
##            slideText = ' '.join([tok.strip() for tok in slideText.split(" ") if tok.isalnum()])
##
##            fout.write(str(time) + '\n')
##            fout.write("slide\n")
##            fout.write(slideText + '\n') 
##            numConsecWritingFrames = 0
##            detectedWriting = False
##            detectedWritingTime = ""
##          elif is_writing_frame(dpix, dreg):
##            # indicates minor changes in screen
##            numConsecWritingFrames += 1
##            if len(detectedWritingTime) == 0:
##              detectedWritingTime = time
##            if MIN_WRITING_FRAMES <= numConsecWritingFrames \
##                and not detectedWriting:
##              fout.write(detectedWritingTime + '\n')
##              fout.write("writing\n")
##              fout.write("\n")
##              detectedWriting = True
##    fout.close()
