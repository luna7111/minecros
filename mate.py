from flask import Flask, render_template, request

import os
from os.path import isfile, join
import csv

import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

import threading

import socket

import qrcode

import pyautogui

def get_local_ip():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		ip = s.getsockname()[0]
		s.close()
		return ip
	except:
		return "127.0.0.1"

macro_list_files = os.listdir("./macro_lists")

macro_button_names = []
for file in macro_list_files:
	macro_button_names.append(os.path.splitext(file)[0])

for name in macro_button_names:
	print(name)

flask_app = Flask(__name__)
print (type(flask_app))
@flask_app.route("/")
def home():
	return render_template("index.html", macro_file_names=macro_list_files, button_names=macro_button_names)

@flask_app.route("/<filename>", methods=['GET', 'POST'])
def macro_filename(filename):
	if request.method == 'POST':
		macro_command = request.form.get('macro')
		print (macro_command)
		for c in macro_command:
			if c == '/':
				pyautogui.hotkey('shift', '7')
			elif c == '\\':
				pyautogui.press('enter')
			else:
				pyautogui.write(c)
	with open("./macro_lists/" + filename + ".csv") as f:
		reader = csv.reader(f)
		data = list(reader)
	
	return render_template("macro_page.html", macros=data, macro_file_names=macro_list_files, button_names=macro_button_names)

#@flask_app.route("/<filename>/run_macro", methods=['POST'])
#def run_macro():
#	macro_id = request.form.get('macro')
#	if macro_id:
#		print(macro_id)
#	return redirect(url_for('index'))

def gen_qr():
	img = qrcode.make("http://" + get_local_ip() + ":5000")
	img.save("./MateGui/qr.png")

def run_qt():
	gen_qr()
	qt_app = QGuiApplication(sys.argv)
	engine = QQmlApplicationEngine()
	engine.addImportPath(sys.path[0])
	engine.loadFromModule("MateGui", "Main")
	if not engine.rootObjects():
		sys.exit(-1)
	exit_code = qt_app.exec()
	del engine
	sys.exit(exit_code)

def run_flask():
		flask_app.run(host=get_local_ip(), port=5000)

if __name__ == "__main__":
		flask_thread = threading.Thread(target=run_flask, daemon=True)
		flask_thread.start()
		run_qt()

