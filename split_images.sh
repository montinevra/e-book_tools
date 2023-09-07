#!/bin/bash
#
#  mogrify -rotate 270 *.jpg
convert page*.jpg -crop 50%x100% page%03d.jpg
