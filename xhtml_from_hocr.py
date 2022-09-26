#!/usr/bin/env python3
import os as OS
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
			print(f'<a title="{page_num}" id="p{page_num}" epub:type="pagebreak"></a>', end="")
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


def split_prefix_num(name: str):
	idx: int = 0

	for c in reversed(name):
		if not c.isdigit():
			break
		idx += 1
	file_prefix: str = name[:-idx]
	num: int = int(name[-idx:])
	return file_prefix, num


def parse_file(file):
	global parser
	global is_new_page
	global page_num
	global prefix

	is_new_page = True
	name: str = OS.path.splitext(OS.path.basename(file.name))[0]
	file_prefix, page_num = split_prefix_num(name)
	if file_prefix != prefix:
		page_num = roman_from_int(page_num).lower()
	contents = file.read()
	parser.feed(contents)
	file.close()


def main(args):
	global parser
	global prefix

	parser = HtmlFromHocr()
	if args.prefix:
		prefix = args.prefix 
	else:
		prefix = "page"
 
	print(
		"<?xml version='1.0' encoding='utf-8'?>\n" + 
		'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">\n' +
		"<head>\n" + 
		f" <title>{args.title}</title>\n" +
		"</head>\n\n" +
		"<body>\n"
	)
	for j in args.file:
		parse_file(j)
	print("</body>\n</html>\n")
	parser.close()


if __name__ == "__main__":
	import argparse

	argparser = argparse.ArgumentParser()
	argparser.add_argument("file", nargs="*", type=argparse.FileType('r'), help="file(s) to convert")
	argparser.add_argument("-t", "--title", type=str, help="set the title of the ebook")
	argparser.add_argument("-p", "--prefix", type=str, help="Specify the filename prefix. Defaults to 'page'. Filenames with this prefix are considered main body matarial. All other files are considered front material and will be numbered using roman numerals.")
	args = argparser.parse_args()
	main(args)
