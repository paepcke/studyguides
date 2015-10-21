import argparse
import constants
import cv
import cv2
import numpy as np
import os, os.path
import sys

CV_CAP_PROP_FPS = 5

REGION_DP_MIN = 1000
WRITE_DP_MIN = 3000 # number of pixels
WRITE_DP_DENSE_MIN = 5000 # number of pixels
SLIDE_DP_MIN = 100000

SEC_PER_FRAME = 5
SEC_PER_PRINT_UPDATE = 120

REGION_ROWS = 3
REGION_COLS = 3

USE_DP_DENSITY = False

prevFrame_ = np.empty([])

parser = argparse.ArgumentParser()
parser.add_argument('--rerun', action='store_true', dest='rerun', default=False)
parser.add_argument('--verbose', action='store_true', dest='verbose', default=False)
args = parser.parse_args()

def hms_from_seconds(seconds):
  hrs = str(seconds / 3600)
  if len(hrs) < 2: hrs = '0' + hrs
  mins = str((seconds % 3600) / 60)
  if len(mins) < 2: mins = '0' + mins
  secs = str(seconds % 60)
  if len(secs) < 2: secs = '0' + secs
  return str(hrs) + ":" + str(mins) + ":" + str(secs)

def pixel_regions(frame):
  rows, cols, _ = frame.shape
  rows -= 1
  cols -= 1
  x = [i * rows / REGION_ROWS for i in range(0, REGION_ROWS + 1)]
  y = [i * cols / REGION_COLS for i in range(0, REGION_COLS + 1)]
  regions = []
  for i in range(0, REGION_ROWS):
    for j in range(0, REGION_COLS):
      region = ((x[i], x[i + 1]), (y[j], y[j + 1]))
      regions.append(region)
  return regions

def delta_pixels_regions(frame):
  global prevFrame_
  if prevFrame_ == None or len(prevFrame_.shape) == 0:
    # prev frame is empty
    prevFrame_ = frame
    return (0, 0)
  
  diff = frame - prevFrame_
  prevFrame_ = frame
  pixelsCount = 0
  regionCount = 0
  for dx, dy in pixel_regions(frame):
    diffRegion = diff[dx[0]:dx[1], dy[0]:dy[1], :]
    delta = np.count_nonzero(diffRegion)
    pixelsCount += delta
    if REGION_DP_MIN <= delta:
      regionCount += 1
  if regionCount == 0:
    regionCount = REGION_ROWS * REGION_COLS
  return (pixelsCount, regionCount)

def delta_pixels(frame):
  global prevFrame_
  if frame == None:
    return 0
  elif prevFrame_ == None or len(prevFrame_.shape) == 0:
    # prev frame is empty
    prevFrame_ = frame
    return 0
  elif not prevFrame_.shape == frame.shape:
    prevFrame_ = frame
    return reduce(lambda x, y: x*y, frame.shape)

  diff = frame - prevFrame_
  prevFrame_ = frame
  r, g, b = cv2.split(diff)
  return np.count_nonzero(r + g + b)

def fetch_videos(directory):
  videos = list()
  for root, _, files in os.walk(directory):
    for f in files:
      if f.endswith(VID_EXT):
        fullpath = os.path.join(root, f)
        if args.verbose:
          print fullpath
        videos.append(fullpath)
  return videos

def fetch_frames(filename):
  basename = os.path.basename(filename).split(VID_EXT)[0]
  os.system("rm -f -r " + constants.FRAME_REL_PATH + basename)
  os.system("mkdir " + constants.FRAME_REL_PATH + basename)

  if args.verbose:
    print("filename = ", filename)
  video = cv2.VideoCapture(filename)
  success, image = video.read()
  framerate = int(video.get(CV_CAP_PROP_FPS))
  frame = 0
  while success:
    success, image = video.read()
    if frame % framerate == 0 and (frame / framerate) % SEC_PER_FRAME == 0:
      # only consider making a file on the second mark
      seconds = frame / framerate
      time = hms_from_seconds(seconds)
      framename = FRAME_REL_PATH + basename + "/time_" + str(time)
      if args.verbose and seconds % SEC_PER_PRINT_UPDATE == 0:
        print "          processing time ", time, " of video" 
      if USE_DP_DENSITY:
        # use the change in pixels by region
        dp, nregions = delta_pixels_regions(image)
        density = dp / nregions
        if SLIDE_DP_MIN <= dp:
          framename += "_slide"
        elif WRITE_DP_DENSE_MIN <= density: # and density <= WRITE_DP_DENSE_MAX:
          framename += "_writing"
        else:
          framename += "_none"
      else:
        # only consider the absolute change in pixels
        dp = delta_pixels(image)
        if SLIDE_DP_MIN <= dp:
          framename += "_slide"
        elif WRITE_DP_MIN <= dp:
          framename += "_writing"
        else:
          framename += "_none"
      cv2.imwrite(framename + IMG_EXT, image)
    if cv2.waitKey(10) == 27:
      # hit ESC key to break loop
      if args.verbose:
        print "josehdz: cv2.waitKey(10) == 27 forced a break"
      break
    frame += 1

if args.rerun:
  videos = fetch_videos(VIDEO_REL_PATH)
  for video in videos:
    fetch_frames(video)
