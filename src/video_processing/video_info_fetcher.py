import constants
import os, os.path
import PIL        
import pytesseract
import string

MIN_WRITING_FRAMES = 6

def get_frame_info(framepath):
  basename = os.path.basename(framepath).split(constants.IMG_EXT)[0]
  tokens = basename.split('_')
  last = len(tokens) - 1
  return (tokens[last - 1], tokens[last])

def is_slide_frame(frameType):
  return frameType == "slide"

def is_writing_frame(frameType):
  return frameType == "writing"

def extract_info(framedir):
  frameInfoFilename = framedir + "info.txt"
  os.system("rm -f " + frameInfoFilename)
  trantab = string.maketrans(string.punctuation, ''.join([" " for _ in string.punctuation]))
  with open(frameInfoFilename, "w") as fout:
    numConsecWritingFrames = 0
    detectedWriting = False
    detectedWritingTime = ""
    for root, _, files in os.walk(framedir):
      for f in files:
        if f.endswith(constants.IMG_EXT):
          time, frameType = get_frame_info(f)
          if is_slide_frame(frameType):
            # TODO: eventually, write slide text here
            #       using python tesseract library
            image = PIL.Image.open(framedir + f)
            slideText = pytesseract.image_to_string(image)
            slideText = slideText.replace("\n", " ")
            slideText = slideText.translate(trantab)
            slideText = ' '.join([tok.strip() for tok in slideText.split(" ") if tok.isalnum()])

            fout.write(str(time) + '\n')
            fout.write("slide\n")
            fout.write(slideText + '\n') 
            numConsecWritingFrames = 0
            detectedWriting = False
            detectedWritingTime = ""
          elif is_writing_frame(frameType):
            # indicates minor changes in screen
            numConsecWritingFrames += 1
            if len(detectedWritingTime) == 0:
              detectedWritingTime = time
            if MIN_WRITING_FRAMES <= numConsecWritingFrames \
                and not detectedWriting:
              fout.write(detectedWritingTime + '\n')
              fout.write("writing\n")
              fout.write("\n")
              detectedWriting = True
    fout.close()

parentDir = constants.FRAME_REL_PATH
for directory in os.listdir(parentDir):
  if not directory[0] == '.':
    print "processing directory ", directory
    extract_info(parentDir + directory + '/')
  

