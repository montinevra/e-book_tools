import PySimpleGUI as sg
import subprocess
import os
import sys


def ocr(files, target_dir):
	subprocess.call(['bash', os.path.join(os.path.dirname(__file__), 'ocr.sh')] + files, cwd=target_dir)


def view_files(path):
	subprocess.run(open_folder_command + [path])


def main(argv):
	lbl_img_select = 'Select images...'
	file_box = sg.Listbox([], select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, horizontal_scroll=True, key='-FILEBOX-', auto_size_text=True, expand_x=True, expand_y=True, s=(64,12))
	target_dir = sg.Input(key='-TARGET_DIR-')
	status_line = sg.Text('', key='-STATUS-')
	layout = [
			[sg.Input(key='-FILES_SELECTED-', enable_events=True, visible=False), sg.FilesBrowse(lbl_img_select), file_box],
			[sg.Text('Destination folder:'), target_dir, sg.FolderBrowse()],
			[sg.Button("OCR!", button_color='green'), status_line, sg.pin(sg.Button('View Files', key='-VIEW_FILES-', visible=False)), sg.Push(), sg.Button("Quit", button_color='red')],
			# [status_line, sg.Button('View Files', key="-VIEW_FILES-", visible=False)],
			]
	window = sg.Window('OCR', layout,  resizable=True, font=('', 16))

	while True:
		event, vals = window.read()
		if event in (sg.WIN_CLOSED, 'Quit'):
			break
		elif event == '-FILES_SELECTED-':
			file_box.update(values=vals[lbl_img_select].split(';'))
		elif event == 'OCR!':
			if target_dir.get() == '':
				status_line.update(value="Please select a destination folder", text_color='orange')
				continue
			target = target_dir.get()
			window.perform_long_operation(lambda: ocr(file_box.get_list_values(), target), '-OCR_FINISHED-')
			status_line.update(value="OCR-ing!", text_color=None)
			window['-VIEW_FILES-'].update(visible=False)
		elif event == '-OCR_FINISHED-':
			status_line.update(value="OCR finished!", text_color='light green')
			# window["-VIEW_FILES-"].update(visible=False)
			window['-VIEW_FILES-'].update(visible=True)
		elif event == '-VIEW_FILES-':
			view_files(target)
	window.close()


open_folder_commands = {
	'darwin': ['open', '--'],
	'linux': ['xdg-open', '--'],
	'win32': ['explorer'],
}
open_folder_command = open_folder_commands[sys.platform]

if __name__ == "__main__":

	main(sys.argv)
