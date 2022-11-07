#!/usr/bin/env python3
import os as OS
from html.parser import HTMLParser
from roman_numeral.roman_numeral import roman_from_int
import html


class HtmlFromHocr(HTMLParser):
	skipped_tags = ["span", "div", "html", "head", "title", "meta", "body"]

	def handle_starttag(self, tag, attrs):
		global is_new_page
		global page_num

		if tag in self.skipped_tags:
			return
		print(f"<{tag}", end = '')
		# for i in attrs:
		# 	print(' ' + i[0] + '="' + i[1] + '"', end = '')
		print(">", end = '')
		if is_new_page:
			print(f'<a title="{page_num}" id="p{page_num}" epub:type="pagebreak"></a>', end="")
			is_new_page = False

	def handle_endtag(self, tag):
		if tag in self.skipped_tags:
			return
		print(f"</{tag}>")
		if tag == "p":
			print("\n")

	def handle_data(self, data):
		if "\n" in data or "\r" in data:
			return
		if data[-1] == "-":
			data = data[0:-1]
			print(html.escape(data), end = "")
		else:
			print(f'{html.escape(data)} ', end = "")


def split_prefix_num(name: str):
	for idx, c in enumerate(reversed(name)):
		if not c.isdigit():
			break
	file_prefix: str = name[:-idx]
	num: int = int(name[-idx:])
	return file_prefix, num


def parse_file(file_path, args, parser):
	global is_new_page
	global page_num

	is_new_page = True
	name: str = OS.path.splitext(OS.path.basename(file_path))[0]
	file_prefix, page_num = split_prefix_num(name)
	if file_prefix != args.prefix:
		page_num += args.foffset
		page_num = roman_from_int(page_num).lower()
	else:
		page_num += args.offset
	with open(file_path, 'r') as file:
		contents = file.read()
		parser.feed(contents)


def print_out(args):
	parser = HtmlFromHocr()
	print(
		"<?xml version='1.0' encoding='utf-8'?>\n" + 
		f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{args.language}" xml:lang="{args.language}">\n' +
		"<head>\n" + 
		f" <title>{args.title}</title>\n" +
		"</head>\n\n" +
		"<body>\n"
	)
	for j in args.file_path:
		parse_file(j, args, parser)
	print("</body>\n</html>\n")
	parser.close()


def main(args):
	if args.output:
		import sys
		with args.output as sys.stdout:
			print_out(args)
	else:
		print_out(args)


if __name__ == "__main__":
	import argparse

	argparser = argparse.ArgumentParser()
	argparser.add_argument("file_path", nargs="*", type=str, help="File(s) to convert.")
	argparser.add_argument("-F", "--foffset", type=int, default=0, help="Same as -O, but for front matter.")
	argparser.add_argument("-l", "--language", type=str, default="en", help="Set the LCID for the document. Defaults to 'en'.")
	argparser.add_argument("-O", "--offset", type=int, default=0, help="Offset the page number of main body matter by this amount. Useful if the filename does not match the page number. For example, if page001.jpg contains page 3, set this to 2. Can be nagative.")
	argparser.add_argument("-o", "--output", type=argparse.FileType('w'), help="Output file. Defaults to stdout.")
	argparser.add_argument("-p", "--prefix", type=str, default="page", help="Specify the filename prefix. Defaults to 'page'. Filenames with this prefix are considered main body matter. All other files are considered front matter and will be numbered using roman numerals.")
	argparser.add_argument("-t", "--title", type=str, help="Set the title of the ebook.")
	args = argparser.parse_args()
	main(args)
