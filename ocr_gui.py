import PySimpleGUI as sg
import subprocess


file_box = sg.Listbox([], select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, horizontal_scroll=True, key='-FILEBOX-', auto_size_text=True, expand_x=True, expand_y=True, s=(64,6))
layout = [
		[sg.Input(key='-FILES_SELECTED-', enable_events=True, visible=False), sg.FilesBrowse('Select files...'), file_box],
		[sg.Button("OCR!"), sg.Push(), sg.Button("Quit")],
		]
window = sg.Window('OCR', layout, size=(600,300), resizable=True)

while True:
	event, values = window.read()
	if event in (sg.WIN_CLOSED, 'Quit'):
		break
	if event == '-FILES_SELECTED-':
		file_box.update(values=values['Select files...'].split(';'))
	if event == 'OCR!':
		subprocess.call(['bash', 'ocr.sh'] + file_box.get_list_values())
window.close()
