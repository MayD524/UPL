import tkinter as tk
from tkinter import ttk
from win10toast import ToastNotifier
from UPL.Core import file_manager as fm
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
