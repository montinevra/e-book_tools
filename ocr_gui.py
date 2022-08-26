import PySimpleGUI as sg
import subprocess
import os


def ocr(files, target_dir):
	subprocess.call(['bash', os.path.join(os.path.dirname(__file__), 'ocr.sh')] + files, cwd=target_dir)


def main(argv):
	file_box = sg.Listbox([], select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, horizontal_scroll=True, key='-FILEBOX-', auto_size_text=True, expand_x=True, expand_y=True, s=(64,12))
	target_dir = sg.Input(key='-TARGET_DIR-')
	status_line = sg.Text('', key='-STATUS-')
	layout = [
			[sg.Input(key='-FILES_SELECTED-', enable_events=True, visible=False), sg.FilesBrowse('Select images...'), file_box],
			[sg.Text('Destination folder:'), target_dir, sg.FolderBrowse()],
			[sg.Button("OCR!", button_color='green'), status_line, sg.Push(), sg.Button("Quit", button_color='red')],
			]
	window = sg.Window('OCR', layout,  resizable=True, font=('', 16))

	while True:
		event, vals = window.read()
		if event in (sg.WIN_CLOSED, 'Quit'):
			break
		elif event == '-FILES_SELECTED-':
			file_box.update(values=vals['Select files...'].split(';'))
		elif event == 'OCR!':
			if target_dir.get() == '':
				status_line.update(value="Please select a destination folder", text_color='orange')
				continue
			window.perform_long_operation(lambda: ocr(file_box.get_list_values(), target_dir.get()), '-OCR_FINISHED-')
			status_line.update(value="OCR-ing!", text_color=None)
		elif event == '-OCR_FINISHED-':
			status_line.update(value="OCR finished!", text_color='light green')
	window.close()


if __name__ == "__main__":
	import sys

	main(sys.argv)
