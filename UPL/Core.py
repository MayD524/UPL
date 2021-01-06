from pathlib import Path
import json
import os

__version__ = "0.1.0"

def PAUSE():
	input("ENTER TO CONTINUE")

def clear():
	os.system("clear" if os.name != "nt" else "cls")

def safe_run(func):
	def wrapper(*args):
		try:
			func(args)
		except Exception as e:
			raise e
	return wrapper


def ainput(prompt=None, outType=None, char_size=None, delim=None, ending=None):
	if outType == None: outType = str if delim == None else list
	if prompt == None: prompt = ""

	inp = input(prompt)
	if inp == "" and outType == None:
		return False

	if outType == list:
		li = []
		tmp = ""
		last = 0

		if delim == None:
			if char_size == None: char_size = 1
			for i in range(len(inp)):
				tmp += inp[i] 

				if last == char_size:
					li.append(tmp)
					tmp = ""
					last = 0
				last += 1
		else:
			li = inp.split(delim)

		return li

	elif ending != None:
		if inp.endswith(ending):
			return outType(inp)
		else:
			raise Exception("Incorrect extention")

	else:
		return outType(inp)

def getHome():
	return str(Path.home())

def scan_dir(dir_name=None, full_dir=False):
	folder = os.listdir(dir_name)
	items = []
	if full_dir == True:
		for i in folder:
			items.append(os.path.join(dir_name, i))
		return items
	else:
		return folder

def switch(cases:dict, val):
	return cases[val] if val in cases.keys() else False

def file_exists(filename):
	return True if os.path.exists(filename) else False

def dir_exists(filename):
	return True if os.path.isdir(filename) else False

class file_manager:

	def getData_json(file):
		if file_exists(file):
			with open(file, "r+") as jsReader:
				return json.load(jsReader)
		else:
			raise Exception(f"File '{file}' not found")

	def write_json(file, data=None, indent=1):
		if file_exists(file) and type(data) == dict or data == None:
			with open(file, "w+") as jsWriter:
				if data == None:
					json.dump({}, jsWriter)
				else:
					json.dump(data, jsWriter,indent=indent)

		else:
			raise Exception(f"Either file does not exist or data is not a dict or NULL")

	def make_json(file):
		if not file_exists(file):
			with open(file, "w+") as wr:
				json.dump({}, wr)
		else:
			raise Exception(f"File '{file}' exists")

	def wipe_json(file):
		if file_exists(file):
			with open(file, "w+") as wr:
				json.dump({}, wr)
		else:
			file_manager.make_json(file)

	def read_file(file):
		if os.path.exists(file):
			tmp = []
			with open(file, "r+") as Reader:
				for i in Reader:
					tmp.append(i)

			return tmp
		else:
			raise Exception(f"File '{file}' was not found")

	def write_file(file, data, mode=None):
		if file_exists(file) and '+' not in mode:
			with open(file, mode if mode != None else "w") as writer:
				writer.write(data)
		else:
			raise Exception(f"File '{file}' was not found")

	def getSize(file):
		if file_exists(file):
			return os.path.getsize(file)

		else:
			raise Exception(f"File '{file}' was not found or cannot be accessed")