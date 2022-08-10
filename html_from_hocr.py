#!/usr/bin/env python3
import os as OS
import glob as GLOB
from html.parser import HTMLParser
from roman_numeral.roman_numeral import roman_from_int


class HtmlFromHocr(HTMLParser):
	skipped_tags = ["span", "div", "html", "head", "title", "meta", "body"]

	def handle_starttag(self, tag, attrs):
		global is_new_page
		global page_num

		if tag in self.skipped_tags:
			return
		print("<" + tag, end = '')
		# for i in attrs:
		# 	print(' ' + i[0] + '="' + i[1] + '"', end = '')
		print(">", end = '')
		if is_new_page:
			print('<a title="' + str(page_num) + '" id="p' + str(page_num) + '" epub:type="pagebreak"></a>', end="")
			is_new_page = False

	def handle_endtag(self, tag):
		if tag in self.skipped_tags:
			return
		print("</" + tag + ">")
		if tag == "p":
			print("\n")

	def handle_data(self, data):
		if "\n" in data or "\r" in data:
			return
		if data[-1] == "-":
			data = data[0:-1]
			print(data, end = "")
		else:
			print(data + ' ', end = "")


def parse_file(t_path):
	global parser
	global is_new_page
	global page_num

	file = open(t_path, "r")
	is_new_page = True
	prefix = OS.path.splitext(OS.path.basename(t_path))[0][:-3]
	page_num = OS.path.splitext(OS.path.basename(t_path))[0][-3:]
	if prefix != "page":
		page_num = roman_from_int(int(page_num)).lower()
	contents = file.read()
	parser.feed(contents)
	file.close()


def main(t_argv):
	global parser

	if len(t_argv) > 1:
		parser = HtmlFromHocr()
		print(
			"<?xml version='1.0' encoding='utf-8'?>\n" + 
			'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">\n' +
			"<head>\n" + 
  			" <title></title>\n" +
			"</head>\n\n" +
			"<body>\n"
		)
		for j in t_argv[1:]:
			for i in GLOB.glob(j):
				if OS.path.isdir(i):  
					# print(i + " is a directory")  
					for k in OS.listdir(i):
						parse_file(i + k)  
				elif OS.path.isfile(i):  
					parse_file(i)
		print("</body>\n</html>\n")
		parser.close()


if __name__ == "__main__":
	import sys

	main(sys.argv)