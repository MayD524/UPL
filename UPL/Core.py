from pathlib import Path
import urllib.request
import cryptocode
import subprocess
import webbrowser
import zipfile
import hashlib
import getpass
import uuid
import json
import sys
import ast
import os

__version__ = "0.1.6"

"""
	Moved socket stuff to upl_socket.py
	it was getting to be a little too big to stay
	in core.
"""




"""
Pauses and waits for user to press
enter
"""
def PAUSE():
	input("ENTER TO CONTINUE")

def getUser() -> str:
	return getpass.getuser()

def make_hash(data):
	hash_obj = hashlib.sha256(data.encode('utf-8'))
	return hash_obj.hexdigest()

def insert(source:list, newData:any) -> list:
	if newData not in source:
		return source.append(newData)
	else:
		print(f"{newData} already in source")
		return False

def removeVal(source, index):
	newList = []
	if type(index) == int:
		if index <= len(source):
			index = source[index]
		else:
			print(f'{index} out of range {len(source)}')
			return False
	for i in range(len(source)):
		if source[i] != index:
			newList.append(source[i])
	return newList

def progressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = '\r'):
	"""
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """

	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
	if iteration == total: 
		print()

def char_frequency(string:str, exclude=None, include=None) -> dict:
	characters = {}

	for i in string:
		if exclude != None and i in exclude:
			continue
		if include != None and i not in include:
			continue
		if i in characters:
			characters[i] += 1
		else:
			characters[i] = 1

	return characters
"""
clears console
"""
def clear():
	os.system("clear" if os.name != "nt" else "cls")

def removeStart(string:str,Length:int) -> str:
	return string[Length:]

def removeEnding(string:str, Length:int) -> str:
	if Length > 0:
		Length = Length * -1
	return string[:Length]

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

def currentDir():
	return os.getcwd()

def removeEmpty(array:list) -> list:
	exitArray = []
	for i in range(len(array)):
		if array[i] == '\n':
			continue
		if len(array[i]) != 0:
			exitArray.append(array[i])

	return exitArray	

def checkIn(string:str, array:list) -> str:
	for i in array:
		if i in string:
			return i
	return False ## returning that no item in the array is in string

def asplit(string:str, number=2) -> list:
	"""
		Splits a string ever n characters -> default is 2
	"""

	return [string[i:i+number] for i in range(0, len(string), number)]

## removes a character from string
def exclude(string=None, remove=" "):
	if string != None:
		if remove in string:
			return string.replace(remove, "")
		else:
			## remove not in string
			return string
	else:
		## empty string
		return False

"""
ainput > is input with options to do common 
actions with console prompt 
"""
def ainput(prompt=None, outType=None, min_size=None, char_size=None, delim=None, ending=None):
	if outType == None: outType = str if delim == None else list
	if prompt == None: prompt = ""

	inp = input(prompt)

	if min_size != None:
		if not len(inp) >= min_size:
			return False
			
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

	
	return outType(inp)

class licenceManager:
    def __init__(self, magic):
        self.magic = magic

    def make_check(self, string):
        end = 0
        for i in string:
            end += ord(i)
        
        end += self.magic

        return end

    def compair_keys(self, check, string):
        stringSum = self.make_check(string)
        return check == stringSum

class dataTypes:
	def strDict(string):
		try:
			return json.loads(string)
		except json.JSONDecodeError as e:
			return e

	def strList(string):
		return ast.literal_eval(string)


	def dictFormat(dct):
		try:
			return json.dumps(dct)
		except Exception as e:
			print(e)


class JSONTABLE:
	def __init__(self, new=True, data=None):
		if new != True:
			self.jsonData = data
			if "UUID" in self.jsonData.keys:
				self.UUID = self.jsonData["UUID"]
			else:
				self.UUID = generate_uuid()
				self.jsonData["UUID"] = self.UUID
		else:
			self.UUID = generate_uuid()
			self.jsonData = {
				"UUID":self.UUID,
				"NAME":f"{self.UUID}.json"
			}
	
	def encrypt_data(self, data, passw):
		return cryptocode.encrypt(data, passw)


	def table_add(self, table_name, key=None, value=None):
		if self.table_exists(table_name):
			pass

		else:
			return False

	def table_exists(self, table_name):
		return table_name in self.jsonData.keys()

	def create_table(self, table_name, encrypt=False):
		flags = [encrypt]
		self.jsonData[table_name] = {"Flags":flags}


"""
	Basic grid type, will
	expand later
"""
class grid:
	def __init__(self, data:list):
		self.main_grid = [data]

	def __str__(self):
		return str(self.main_grid)

	def append(self, val:list):
		self.main_grid.append(val)

	def remove(self, index):
		del self.main_grid[index]

"""
getHome > returns current users 
home directory "C:\\Users\\Username"
"""
def getHome():
	return str(Path.home())

"""
generate_uuid > returns a uuid
"""
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

"""
switch case implimentation in python
"""
def switch(cases:dict, val):
	return cases[val] if val in cases.keys() else False

"""
checks if file/dir exists
"""
def file_exists(filename):
	return True if os.path.exists(filename) else False

def dir_exists(filename):
	return True if os.path.isdir(filename) else False

"""
py_tools class is for python tools
such as PIP and installing packages
at runtime
"""
class py_tools:
	def pip_install(package):
		try:
			if type(package) == str:
				subprocess.check_call([sys.executable, "-m", "pip", "install", package])
			elif type(package) == list:
				subprocess.check_call(package)
		except Exception as e:
			print(e)

	def pip_install_mass(package):
		for pack in package:
			try:
				subprocess.check_call([sys.executable, "-m", "pip", "install", pack])
			except Exception as e:
				print(e)

"""
system_tools class is for common
system calls and actions 
"""
class system_tools:

	def make_call(call):
		subprocess.check_call(call)


"""
upl_web class is for 
web tasks
"""
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

"""
upl_math class is for
math and most return a
lambda function
"""
class upl_math:

	def geometric(first, common):
		return lambda n : first * (common ** (n - 1))

	def arithmetic(first, common):
		return lambda n : first + common * (n - 1)


"""
file_manager class is for
file management and directory
with json support
"""
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

	def make_file(file):
		if not file_exists(file):
			with open(file, "w+") as f:pass
			return True
		else:
			return False
	def write_file(file, data, mode=None):
		if file_exists(file):
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

	## Hash
	def file_hash(file):
		if file_exists(file):
			hashs = []
			with open(file, "r") as hash_reader:
				hsmd5 = hashlib.md5(hash_reader.read().encode('utf-8'))
				hssha1 = hashlib.sha1(hash_reader.read().encode('utf-8'))
				hashs.extend([hsmd5.hexdigest(),hssha1.hexdigest()])
				return hashs
		else:
			return f"{file} was not found"
		
	## General
	def renameFile(filename, newFilename):
		if file_exists(filename):
			os.rename(filename, newFilename)
			return True
		else:
			return f"{filename} does not eixst"

	def delete_file(filename):
		if file_exists(filename):
			os.remove(filename)
			return True
		else:
			return f"{filename} does not exist"

	def create_dir(dir_name):
		if dir_exists(dir_name):
			return f"{dir_name} already exists"
		else:
			os.makedirs(dir_name)
			return True

	def getSize(file):
		if file_exists(file):
			return os.path.getsize(file)

		else:
			return f"File '{file}' was not found or cannot be accessed"