#!/bin/bash

for FILE in "$@"; do
	OUTPUT=$(basename "${FILE%.*}")
 	tesseract "${FILE}" $OUTPUT --oem 2 hocr
done