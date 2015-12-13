============================================================
file: edit_distance.py

This file is used for its function "getSpelling" which gets 
the likely candidates of the arg word based on edit distance.
It assumes that there is a sequence of --window (default: 3)
correct characters in the arg word, and returns the best word
from the gold vocabulary. If there are ties, it returns a 
random choice among the best. If the arg word has no matches
or is less than --window characters long, "" is returned.

The gold vocabulary is assumed to be the list of words used
in the closed caption files.

creates file in directory named: gold-vocabulary.txt

============================================================
file: frame_fetcher.py

This reads all of the videos in the specified video directory
and breaks them apart frame by frame. It also checks for the
pixel changes between frames and appends the information to
the frame file name. The frames are saved in a directory.

--rerun-all : 
    runs all video processing again
--rerun : 
    must be specified, in addition to --continue_after
--continue-after <filename> : 
    must be specified to run anything,
    because it takes a filename from which to continue
--verbose : 
    see printed progress

============================================================
file: video_info_fetcher.py

This file reads all of the frames in the frame directory. If
specified, it also runs OCR to pull slide text for each frame. 
Also, if specified, it creates more files that contain only 
the information from frames that contain new slides and new 
writing.

New files in each video frame folder:

  raw_slide_text.txt: contains the frame information, which was
      pulled from the frame image files.
    --> <HH:MM:SS>   (timestamp)
    --> <delta_pix>  (num pixels that changed from last frame)
    --> <delta_reg>  (num regions with many pixel changes)
    --> <slide_text> (OCR raw text **caution: contains newlines**)

  slide_text.txt: contains the frame information, which was
      pulled from the frame image files.
    --> <HH:MM:SS>   (timestamp)
    --> <delta_pix>  (num pixels that changed from last frame)
    --> <delta_reg>  (num regions with many pixel changes)
    --> <slide_text> (OCR text w/ only spaces and alpha-num)

  unique_slide_info.txt: contains condensed frame information,
      which was pulled from the slide_text.txt file.
    --> <HH:MM:SS>   (timestamp)
    --> <event>      (slide or writing)
    --> <slide_text> (OCR text w/ only spaces and alpha-num)
    --> <\n>

Flags to specify:

--continue-after <dirname> :
    continues after some directory in the frames directory
--rerun-ocr :
    reruns OCR that extracts text for each frame and creates 
    the slide_text.txt and raw_slide_text.txt file. SLOW PROCESS
--rerun-labels :
    reruns the event labeling and creates the unique_slide_info.txt
    file, but requires up-to-date slide_text.txt file
--verbose :
    prints the progress for each directory containing the
    lectures' frames.

============================================================
file: caption_fetcher.py

Creates files with parallel lines for slide text and caption
text. This depends on the folder and lecture names to be the 
exact same. There are two files created:

  both.txt : contains the information from the closed caption
      file and unique_slide_info.txt and follows the structure:
    --> <HH:MM:SS>     (timestamp)
    --> <event>        (slide or writing)
    --> <slide_text>   (slide text)
    --> <caption_text> (all caption text in this time interval)
    --> <\n>

  both_cleaned.txt : contains almost the exact same information
      in both.txt but the slide text is spell corrected using
      the edit_distance.py package we wrote earlier
    --> <HH:MM:SS>     (timestamp)
    --> <event>        (slide or writing)
    --> <slide_text>   (spell-corrected slide text)
    --> <caption_text> (all caption text in this time interval)
    --> <\n>

============================================================
file: constants.py

Specifies constants needed to run all of these files. Only
need to change this document as the file structure changes.
