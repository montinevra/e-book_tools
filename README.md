# e-book_tools

## ocr.sh
Runs Tesseract on all the specified files. Requires Tesseract: https://github.com/tesseract-ocr/tesseract

    bash ocr.sh file1 [file2 ... fileN]

## ocr_gui.py
A gui frontend for the above script. Requires PySimpleGUI: https://www.pysimplegui.org/en/latest/

    python3 ocr_gui.py

## xhtml_from_hocr.py
Converts .hocr files to xhtml. Removes hocr-related data and just leaves the content with basic xhtml formatting. Adds a pagebreak tag (used in epub) based on the filename. 

    python3 html_from_hocr.py file1 [file2 ... fileN]

Outputs directly to the shell. Redirect it if you want to save to a file.

	python3 html_from_hocr.py file1 [file2 ... fileN] > some_file.xhtml
