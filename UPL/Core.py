from pathlib import Path
from _thread import *
import urllib.request
import socketserver
import subprocess
import webbrowser
import zipfile
import hashlib
import socket
import uuid
import json
import sys
import ast
import os

__version__ = "0.1.6"

"""
Pauses and waits for user to press
enter
"""
def PAUSE():
	input("ENTER TO CONTINUE")

def make_hash(data):
	hash_obj = hashlib.sha256(data.encode('utf-8'))
	return hash_obj.hexdigest()

def uplSort(unsorted:list) -> list:
	sorted = []

	for i in range(len(unsorted)):
		tmp = [] ## reset tmp
		tmp.append(int(ord(unsorted[i][[x for x in range(len(unsorted[i]))]])))
		print(tmp)


"""
clears console
"""
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

def currentDir():
	return os.getcwd()
"""
ainput > is input with options to do common 
actions with console prompt 
"""
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

	##else: else not needed here
	return outType(inp)

"""
DataTypes class has some useful tools
to make data easier to handle.
"""
class dataTypes:
	def strDict(string):
		try:
			return json.loads(string)
		except json.JSONDecodeError as e:
			return e

	def strList(string):
		return ast.literal_eval(string) ## fixed (did nothing before) - Ryan


	def dictFormat(dct):
		try:
			return json.dumps(dct)
		except Exception as e:
			print(e)
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
	## added if so dir_name cant be none 
	if dir_name != None:
		folder = os.listdir(dir_name)
		items = []
		if full_dir == True:
			for i in folder:
					items.append(os.path.join(dir_name, i))
			return items
		## else not needed here
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
	## might add more to this, I haven't had much use for anything here
	## so might just make make_call() into it's own func
	def make_call(call):
		subprocess.check_call(call)


"""
upl_web class is for 
web tasks
"""
class upl_web:
	def download_url(url=None, outdir=None): ## returns void
		if url != None:
			## setting a default outdir - will break without
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

"""
	UPL Socket support
	for both client and server side
"""
class upl_socket:
	"""
	Ran on client side
	"""
	class client:
		## add opcodes to cli side
		def __init__(self, hostname, port):
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((hostname, port))

		def sendInfo(self, data):
			if type(data) != bytes:
				data = data.encode('ascii')

			self.sock.send(data)

		def formPacket(self, opCode, data):
			return f"{opCode}:{data}:{str(type(data))}".encode('ascii')

		def getdata(self, buffer):
			return self.sock.recv(buffer)

		def onStart(self):
			loc = []
			local = socket.gethostname()
			localhash = make_hash(local)
			loc.extend([local, localhash])
			return loc

		def uplClose(self):
			self.sock.close()
	"""
		Server actions
		Things that the server can do
	"""

	class serverActions:
		def __init__(self, conn, addr, threadID, config):
			self.conn = conn
			self.addr = addr
			self.threadID = threadID
			self.config = config
			self.uConfig = fm.getData_json(self.config["users"])
			self.securityProf = fm.getData_json((self.config["security"]))

			self.opCodeDict = {
				0: self.connQuit,
				1: self.checkUINFO,
				7: self.setPerm,
				8: self.mkdir,
				9: self.makeFile,
				10: self.writeOTHER,
				11: self.writeJSON,
				12: self.renameFile,
				15: self.getDATA,
				16: self.getJSON
			}

		def connQuit(self):
			self.conn.close()

		def checkUINFO(self, data):
			if data[1] in self.uConfig.keys():
				if data[0] == self.uConfig["dev_name"] and self.uConfig["dev_hash"] == UPL.Core.make_hash(
						data[0] + self.uConfig["UUID"]):
					self.conn.send(b"returned true")
			else:
				tmp = {}
				uuid = UPL.Core.generate_uuid()
				permFile = f"no_touch\\{data[1]}.{uuid}.txt"
				fm.make_file(permFile)
				tmp[data[1]] = {"dev_name": data[0], "UUID": uuid, "dev_hash": UPL.Core.make_hash(data[0], uuid),
								"permFile": permFile}

		def renameFile(self, data):
			if fm.renameFile(data[0], data[1]):
				self.conn.send(bf"Renamed {data[0]} to {data[1]}")
			else:
				self.conn.send(bf"Could not find {data[0]}")

		def mkdir(self, dirname):
			if UPL.Core.dir_exists(dirname):
				self.conn.send(b"dir exists")
			else:
				fm.create_dir(dirname)
				self.conn.send(b"dir made")

		## will add stuff to this later not important yet
		def setPerm(self, data):
			pass

		def getDATA(self, data):
			file_data = "".join(fm.read_file(data))
			file_data = file_data.encode('ascii')
			self.conn.send(file_data)

		def getJSON(self, data):
			if UPL.Core.file_exists(data[0]):
				jsonData = fm.getData_json(data[0])
				data = jsonData[data[1]]
				self.conn.send(str(data).encode('ascii'))

		def makeFile(self, data):
			if UPL.Core.file_exists(data):
				self.conn.send(b"That file already exists")
			else:
				fm.make_file(data)

		def writeOTHER(self, data):
			print(data)
			data, file = data.split("/")
			if UPL.Core.file_exists(file):
				if "not touch" in file or "ser":
					self.conn.send(b"cant edit that file")
				else:
					fm.write_file(file, data=data)
					self.conn.send(b"wrote file")

		def writeJSON(self, data):
			data, file = data.split("/")
			jsData = UPL.Core.dataTypes.strDict(data)
			if UPL.Core.file_exists(file):
				if "no touch" in file:
					fm.write_json(jsData)

		def process(self, opCode, data):
			func = UPL.Core.switch(self.opCodeDict, opCode)
			func(data)

	"""
	Ran on server side
	"""
	class server:
		def __init__(self, host, port):
			self.ServerSocket = socket.socket()
			self.config = file_manager.getData_json("no_touch/config.json")
			self.ThreadCount = 0

			try:
				self.ServerSocket.bind((host, port))
			except socket.error as e:
				print(str(e))
				return

			print("Waiting for connections...")
			self.ServerSocket.listen(5)

		def handler(self, actClass, data):
			data = data.split(":")
			opCode = int(data[0])
			uData = data[1]
			dType = data[2]

			if 'list' in dType:
				uData = UPL.Core.dataTypes.strList(uData)
			elif 'dict' in dType:
				uData = UPL.Core.dataTypes.strDict(uData)
			elif 'str' in dType:
				uData = str(uData)
			elif 'float' in dType:
				uData = float(uData)
			elif 'int' in dType:
				uData = int(uData)
			elif 'bool' in dType:
				uData = bool(uData)

			actClass.process(opCode, uData)
			
		## when connections are forced off it can throw an error but said error is not bad
		def threaded_client(self, connection, addr, c):
			SA = serverActions(connection, addr, c, self.config)
			connection.send(str.encode('Welcome to the Server\n'))
			while True:
				data = connection.recv(2048).decode('ascii')
				self.handler(SA, data)
				reply = 'Server Says: You are thread: ' + str(c)
				if not data:
					break
				connection.sendall(str.encode(reply))
			self.ThreadCount -= 1
			print(f"Disconnected from: {addr[0]}:{str(addr[1])}")
			print(f"Thread Count: {self.ThreadCount}")
			connection.close()

		def main(self):
			while True:
				Client, address = self.ServerSocket.accept()
				print('Connected to: ' + address[0] + ':' + str(address[1]))
				start_new_thread(self.threaded_client, (Client, address, self.ThreadCount,))
				self.ThreadCount += 1
				print('Thread Number: ' + str(self.ThreadCount))
			# break
			self.ServerSocket.close()
