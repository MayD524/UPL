from pathlib import Path
import urllib.request
import webbrowser
import zipfile
import uuid
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

def isEmpty(item:dict) -> bool:
	return False if not item else True

def total_upper(string):
	return sum(map(str.isupper, string))

def open_web(url=None, new=1):
	webbrowser.oepn(url, new=1)

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

def generate_uuid():
	return str(uuid.uuid4())

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

class upl_web:
	def download_url(url=None, outdir=None):
		if outdir == None:
			outdir = f"{getHome()}\\Downloads"
		urllib.request.urlretrieve(url, outdir)

	def url_exist(url):
		"""
		Checks that a given URL is reachable.
		:param url: a URL
		:rtype: bool
		"""
		req = urllib.request.Request(url)
		req.get_method = lambda: "HEAD"

		try:
			urllib.request.urlopen(req)
			return True
		except urllib.request.HTTPError:
			return False

	def open(url):
		if self.url_exist(url):
			webbrowser.oepn(url, new=1)
		else:
			return "Cannot Find That URL"

class upl_math:

	def geometric(first, common):
		return lambda n : first * (common ** (n - 1))

	def arithmetic(first, common):
		return lambda n : first + common * (n - 1)

class file_manager:
	## Json files
	def getData_json(file):
		if file_exists(file):
			with open(file, "r+") as jsReader:
				return json.load(jsReader)
		else:
			return f"File '{file}' not found"

	def write_json(file, data=None, indent=1):
		if file_exists(file) and type(data) == dict or data == None:
			with open(file, "w+") as jsWriter:
				if data == None:
					json.dump({}, jsWriter)
				else:
					json.dump(data, jsWriter,indent=indent)

		else:
			return f"Either file does not exist or data is not a dict or NULL"

	def make_json(file):
		if not file_exists(file):
			with open(file, "w+") as wr:
				json.dump({}, wr)
		else:
			return f"File '{file}' exists"

	def wipe_json(file):
		if file_exists(file):
			with open(file, "w+") as wr:
				json.dump({}, wr)
		else:
			file_manager.make_json(file)

	## Other files
	def read_file(file):
		if os.path.exists(file):
			tmp = []
			with open(file, "r+") as Reader:
				for i in Reader:
					tmp.append(i)

			return tmp
		else:
			return f"File '{file}' was not found"

	def write_file(file, data, mode=None):
		if file_exists(file) and '+' not in mode:
			with open(file, mode if mode != None else "w") as writer:
				writer.write(data)
		else:
			return f"File '{file}' was not found"

	## Zip files
	def unzip(file):
		if file_exists(file):
			try:
				with zipfile.ZipFile(file, "r") as zip_ref:
					zip_ref.extractall()
			except Exception as e:
				return e
		else:
			return "File does not exist"

	def zip_dir(folderPath=None, zipPath=None):
		if dir_exists(folderPath):
			if zipPath == None:
				zipPath = f"{generate_uuid()}.zip"

			with zipfile.ZipFile(zipPath, "w") as zipf:
				len_dir = len(folderPath)
				for root, _, files in os.walk(folderPath):
					for file in files:
						filepath = os.path.join(root, file)
						zipf.write(filepath, filepath[len_dir:])

		else:
			return f"{folderPath} is not a folder"
	def zip_file(file=None, zipPath=None):
		if file_exists(file):
			if zipPath == None:
				zipPath = f"{generate_uuid()}.zip"
			with zipfile.ZipFile(zipPath, "w") as zipW:
				zipW.write(file)
		else:
			return f"{file} is not a file"
	## General
	def getSize(file):
		if file_exists(file):
			return os.path.getsize(file)

		else:
			return f"File '{file}' was not found or cannot be accessed"