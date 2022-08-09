#!/usr/bin/env python3
import os as OS
import glob as GLOB
from html.parser import HTMLParser


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
			print('<a title="p' + str(page_num) + '" id="p' + str(page_num) + '" epub:type="pagebreak"></a>', end="")
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
	page_num = OS.path.splitext(OS.path.basename(t_path))[0][-3:]
	contents = file.read()
	parser.feed(contents)
	file.close()


def main(t_argv):
	global parser

	if len(t_argv) > 1:
		parser = HtmlFromHocr()
		for j in t_argv[1:(len(t_argv))]:
			for i in GLOB.glob(j):
				if OS.path.isdir(i):  
					# print(i + " is a directory")  
					for k in OS.listdir(i):
						parse_file(i + k)  
				elif OS.path.isfile(i):  
					parse_file(i)
		parser.close()


if __name__ == "__main__":
	import sys

	main(sys.argv)