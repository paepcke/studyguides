import argparse
import constants
import cv
import cv2
import multiprocessing
import numpy as np
import os, os.path
import sys

CV_CAP_PROP_FPS = 5

USE_DP_DENSITY = True

prevFrame_ = np.empty([])

parser = argparse.ArgumentParser()
parser.add_argument('--rerun', action='store_true', dest='rerun', default=False)
parser.add_argument('--rerun-all', action='store_true', dest='rerun_all', default=False)
parser.add_argument('--continue-after', action="store", dest="continue_after", default="")
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

def pixel_regions(frame):
  rows, cols, _ = frame.shape
  rows -= 1
  cols -= 1
  x = [i * rows / constants.REGION_ROWS for i in range(0, constants.REGION_ROWS + 1)]
  y = [i * cols / constants.REGION_COLS for i in range(0, constants.REGION_COLS + 1)]
  regions = []
  for i in range(0, constants.REGION_ROWS):
    for j in range(0, constants.REGION_COLS):
      region = ((x[i], x[i + 1]), (y[j], y[j + 1]))
      regions.append(region)
  return regions

def delta_pixels_regions(frame):
  global prevFrame_
  if not USE_DP_DENSITY:
    dp = delta_pixels(frame)
    return (dp, -1)
  elif frame == None:
    return (0, 0)
  elif prevFrame_ == None or len(prevFrame_.shape) == 0:
    # prev frame is empty
    prevFrame_ = frame
    return (0, 0)
  elif not prevFrame_.shape == frame.shape:
    prevFrame_ = frame
    pixelsCount = reduce(lambda x, y: x*y, frame.shape)
    regionCount = constants.REGION_ROWS * constants.REGION_COLS
    return (pixelsCount, regionCount)
  diff = frame - prevFrame_
  prevFrame_ = frame
  pixelsCount = 0
  regionCount = 0
  for dx, dy in pixel_regions(frame):
    diffRegion = diff[dx[0]:dx[1], dy[0]:dy[1], :]
    delta = np.count_nonzero(diffRegion)
    pixelsCount += delta
    if 0 < delta:
      regionCount += 1
  if regionCount == 0:
    regionCount = constants.REGION_ROWS * constants.REGION_COLS
  return (pixelsCount, regionCount)

def fetch_videos(directory):
  videos = list()
  for root, _, files in os.walk(directory):
    for f in files:
      if f.endswith(constants.VID_EXT):
        fullpath = os.path.join(root, f)
        if args.verbose:
          print fullpath
        videos.append(fullpath)
  return videos

def fetch_frames(filename):
  basename = os.path.basename(filename).split(constants.VID_EXT)[0]
  os.system("rm -f -r " + constants.FRAME_REL_PATH + basename)
  os.system("mkdir " + constants.FRAME_REL_PATH + basename)

  if args.verbose:
    print("filename = ", filename)
  video = cv2.VideoCapture(filename)
  success, image = video.read()
  framerate = int(video.get(CV_CAP_PROP_FPS))
  frame = 0
  maxRegions = constants.REGION_ROWS * constants.REGION_COLS
  while success:
    success, image = video.read()
    if frame % framerate == 0 and (frame / framerate) % constants.SEC_PER_FRAME == 0:
      # only consider making a file on the second mark
      seconds = frame / framerate
      time = hms_from_seconds(seconds)
      framename = constants.FRAME_REL_PATH + basename + "/time_" + str(time)

      print "============================="
      print "framerate: ", framerate
      print "frame: ", frame
      print "seconds: ", seconds
      print "time: ", time

      if args.verbose and seconds % constants.SEC_PER_PRINT_UPDATE == 0:
        print "          processing time ", time, " of video" 
      # use the change in pixels by region
      dp, nregions = delta_pixels_regions(image)
      framename = framename + "_" + str(dp) + "_" + str(nregions)
      cv2.imwrite(framename + constants.IMG_EXT, image)
    if cv2.waitKey(10) == 27:
      # hit ESC key to break loop
      if args.verbose:
        print "josehdz: cv2.waitKey(10) == 27 forced a break"
      break
    frame += 1

last_good_video = '../../data/video_lectures/08-07-slr-improvements.mp4'

if args.rerun:
  videos = fetch_videos(constants.VIDEO_REL_PATH)
  shouldProcess = False or args.rerun_all
  for video in videos:
    if shouldProcess:
      if args.verbose:
        print "processing video: ", video
      fetch_frames(video)
    elif args.continue_after == video:
      shouldProcess = True
