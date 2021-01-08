import tkinter as tk
from tkinter import ttk
from win10toast import ToastNotifier
from UPL.Core import file_manager as fm
from UPL import Core as cr
import pyautogui
import calendar
import os

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)


def popup(msg, title="!"):
	popup = tk.Tk()
	popup.wm_title(title)
	label = ttk.Label(popup, text=msg, font = NORM_FONT)
	label.pack(side="top", fill="x")
	B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
	B1.pack()
	popup.mainloop()

def confirm(title="!",text="default", buttons=["OK", "Cancel"]):
	return pyautogui.confirm(title=title, text=text, buttons=buttons)

def prompt(title="!", text="prompt", default=""):
	return pyautogui.prompt(text=text, title=title, default=default)

def password(title="!", text="password", default="", mask="*", rules=None):
	"""
	Rules:
		len -> Minimum length
		upper -> Minimum uppercase letters
		number -> Minimum lowercase letters
		max -> Max length
		special -> Minimum special characters
	"""

	checks = 0

	if not cr.isEmpty(rules):
		return pyautogui.password(text=text, title=title, default=default, mask=mask)
	elif cr.isEmpty(rules) or rules == None:
		issues = []
		pwd = pyautogui.password(text=text, title=title, default=default, mask=mask)

		if "len" in rules.keys():
			if not len(pwd) >= rules["len"]:
				r = rules["len"]
				issues.append(f"Incorrect length : needs -> {r}")
			else:
				checks += 1

		if "upper" in rules.keys():
			if cr.total_upper(pwd) >= rules["upper"]:
				check += 1
			else:
				r = rules["upper"]
				issues.append(f"Incorrect amount of uppercase letters : needs -> {r}")

		if "number" in rules.keys():
			numbers = sum(c.isdigit() for c in pwd)
			if numbers < rules["number"]:
				r = rules["number"]
				issues.append(f"Incorrect amount of numbers : needs -> {r}")

		if "special" in rules.keys():
			numbers = sum(c.isdigit() for c in pwd)
			letters = sum(c.isalpha() for c in pwd)
			others  = len(pwd) - numbers - letters

			if others < rules["special"]:
				r = rules["special"]
				issues.append(f"Incorrect amount of special characters : needs -> {r}")
			else:
				checks += 1	

		if "max" in rules.keys():
			if len(pwd) > rules["max"]:
				r = rules["max"]
				issues.append(f"Password is too long : max -> {r}")
			else:
				checks += 1
		if checks == len(rules.keys()):
			return pwd
		else:
			return issues

def screen_shot(filename=None):
	item = None
	if filename == None:
		item = pyautogui.screenshot()
	else:
		item = pyautogui.screenshot(filename)

	return item

def send_notification(icon=None,threaded=True, title=None, message=None):
	notifier = ToastNotifier()
	if icon != None:
		notifier.show_toast(
			title, 
			message, 
			icon_path=icon,
			threaded=threaded
			)
	else:
		notifier.show_toast(
			title, 
			message,
			threaded=threaded
			)


class TkinterCalendar(calendar.Calendar):
	def select_json(self, json_file):
		self.json = json_file

	def check_events(self, date, button_name):
		data = fm.getData_json(self.json)
		if date in data.keys():
			popup(title="Calendar", msg = f"On {date}, you have {data[date]}")
		else:
			popup(title="Calendar", msg = f"On {date} you have no events.")	
	def formatmonth(self, master, year, month):

		dates = self.monthdatescalendar(year, month)

		frame = tk.Frame(master)

		self.labels = []
		self.button_ids = {}
		for r, week in enumerate(dates):
			labels_row = []
			for c, date in enumerate(week):
				label = tk.Button(frame, text=date.strftime('%Y\n%m\n%d'), command=lambda: self.check_events(date.strftime('%Y-%m-%d'), text))
				label.grid(row=r, column=c)

				if date.month != month:
					label['bg'] = '#aaa'

				if c == 6:
					label['fg'] = 'red'

				labels_row.append(label)
				self.button_ids[label] = date.strftime("%Y-%m-%d")
			self.labels.append(labels_row)
		return frame
