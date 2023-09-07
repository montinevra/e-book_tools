#!/bin/bash
#
# input_file="your_input_file.jpg"
# prefix=$(echo "$input_file" | sed -E 's/(.+)\..+/\1/')
# output_file="${prefix}%03d.${input_file##*.}"
#
# convert "$input_file" -crop 50%x100% +repage "$output_file"

#  mogrify -rotate 270 *.jpg
convert page*.jpg -crop 50%x100% page%03d.jpg
