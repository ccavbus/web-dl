#!/bin/bash
# Bash script that generates film strip video preview using ffmpeg
# You can see live demo: http://jsfiddle.net/r6wz0nz6/2/
# Tutorial on Binpress.com: http://www.binpress.com/tutorial/generating-nice-movie-previews-with-ffmpeg/138

if [ -z "$1" ]; then
    echo "usage: ./movie_preview.sh VIDEO [HEIGHT=120] [COLS=100] [ROWS=1] [OUTPUT]"
    exit
fi

MOVIE=$1
# get video name without the path and extension
MOVIE_NAME=`basename $MOVIE`
OUT_DIR=`pwd`

HEIGHT=$2
COLS=$3
ROWS=$4
OUT_FILENAME=$5

if [ -z "$HEIGHT" ]; then
    HEIGHT=120
fi
if [ -z "$COLS" ]; then
    COLS=100
fi
if [ -z "$ROWS" ]; then
    ROWS=1
fi
if [ -z "$OUT_FILENAME" ]; then
    OUT_FILENAME=`echo ${MOVIE_NAME%.*}_preview.jpg`
fi

OUT_FILEPATH=`echo $OUT_DIR/$OUT_FILENAME`

TOTAL_IMAGES=`echo "$COLS*$ROWS" | bc`

# as a fallback we'll use ffmpeg. This command basically copies this video to /dev/null and it counts
# frames in the process. It's slower (few seconds usually) than ffprobe but works everytime.
NB_FRAMES=`ffmpeg -nostats -i "$MOVIE" -vcodec copy -f rawvideo -y /dev/null 2>&1 | grep frame | awk '{split($0,a,"fps")}END{print a[1]}' | sed 's/.*= *//'`
# I know, that `awk` and `sed` parts look crazy but it has to be like this because ffmpeg can
# `-nostats` By default, `ffmpeg` prints progress information but that would be immediately caught by `grep`
#     because it would contain word `frame` and therefore output of this entire command would be totally
#      random. `-nostats` forces `ffmpeg` to print just the final result.
# `-i "$MOVIE"` Input file
# `-vcodec copy -f rawvideo` We don't want to do any reformating. Force `ffmpeg` to read and write the video as is.
# `-y /dev/null` Dump read video data. We just want it to count frames we don't care about the data.
# `awk ...` The line we're interested in has format might look like `frame= 42` or `frame=325`. Because of that
#     extra space we can't just use `awk` to print the first column and we have to cut everything from the
#     beggining of the line to the term `fps` (eg. `frame= 152`).
# `sed ...` Grab everything after `=` and ignore any spaces

# calculate offset between two screenshots, drop the floating point part
NTH_FRAME=`echo "$NB_FRAMES/$TOTAL_IMAGES" | bc`
echo "capture every ${NTH_FRAME}th frame out of $NB_FRAMES frames"

# make sure output dir exists
mkdir -p $OUT_DIR

FFMPEG_CMD="ffmpeg -loglevel panic -i \"$MOVIE\" -y -frames 1 -q:v 1 -vf \"select=not(mod(n\,$NTH_FRAME)),scale=-1:${HEIGHT},tile=${COLS}x${ROWS}\" \"$OUT_FILEPATH\""
# `-loglevel panic` We don’t want to see any output. You can remove this option if you’re having any problem to see what went wrong
# `-i "$MOVIE"` Input file
# `-y` Override any existing output file
# `-frames 1` Tell `ffmpeg` that output from this command is just a single image (one frame).
# `-q:v 3` Output quality where `0` is the best.
# `-vf \"select=` That's where all the magic happens. Selector function for [video filter](https://trac.ffmpeg.org/wiki/FilteringGuide).
# # `not(mod(n\,58))` Select one frame every `58` frames [see the documentation](https://www.ffmpeg.org/ffmpeg-filters.html#Examples-34).
# # `scale=-1:120` Resize to fit `120px` height, width is adjusted automatically to keep correct aspect ration.
# # `tile=${COLS}x${ROWS}` Layout captured frames into this grid

# print enire command for debugging purposes
# echo $FFMPEG_CMD

echo $OUT_FILEPATH

eval $FFMPEG_CMD
