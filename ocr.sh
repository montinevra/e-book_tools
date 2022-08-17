#!/bin/bash

for FILE in "$@"; do
	OUTPUT=$(basename "${FILE%.*}")
 	tesseract "${FILE}" $OUTPUT hocr
done