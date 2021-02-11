from _thread import *
from UPL import Core
import socket
fm = Core.file_manager

"""
	UPL Socket support
	for both client and server side
"""
conns = {}

class upl_socket:
	
	"""
	Ran on client side
	"""
	"""class client_actions:
		def __init__(self):
			
			self.opCodeDIct = {}

"""
	class client:
		def __init__(self, hostname, port):
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((hostname, port))

		def sendInfo(self, data):
			if type(data) != bytes:
				data = data.encode('ascii')

			self.sock.send(data)

		def formPacket(self, opCode, data):
			return f"{opCode}:{data}:{str(type(data))}".encode('ascii')

		def getdata(self, buffer=1024):
			return self.sock.recv(buffer)

		def onStart(self):
			loc = []
			local = socket.gethostname()
			localhash = Core.make_hash(local)
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
			conns[self.conn] = self.addr
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
				16: self.getJSON,
				17: self.sendData,
				18: self.listcli
			}

		def connQuit(self,data):
			self.conn.close()

		def listcli(self,data):
			self.conn.send(str(conns).encode('ascii'))

		def sendData(self, data):
			pass

		def checkUINFO(self, data):
			if data[1] in self.uConfig.keys():
				if data[0] == self.uConfig["dev_name"] and self.uConfig["dev_hash"] == Core.make_hash(data[0] + self.uConfig["UUID"]):
					self.conn.send(b"returned true")
			else:
				tmp = {}
				uuid = Core.generate_uuid()
				permFile = f"no_touch\\{data[1]}.{uuid}.txt"
				fm.make_file(permFile)
				tmp[data[1]] = {"dev_name": data[0], "UUID": uuid, "dev_hash": Core.make_hash(data[0] + uuid),
								"permFile": permFile}

		def renameFile(self, data):
			if fm.renameFile(data[0], data[1]):
				tmp = f"Renamed {data[0]} to {data[1]}"
				self.conn.send(tmp.encode('ascii'))
			else:
				tmp = f"Could not find {data[0]}"
				self.conn.send(tmp.encode('ascii'))

		def mkdir(self, dirname):
			if Core.dir_exists(dirname):
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
			if Core.file_exists(data[0]):
				jsonData = fm.getData_json(data[0])
				data = jsonData[data[1]]
				self.conn.send(str(data).encode('ascii'))

		def makeFile(self, data):
			if Core.file_exists(data):
				self.conn.send(b"That file already exists")
			else:
				fm.make_file(data)

		def writeOTHER(self, data):
			print(data)
			data, file = data.split("/")
			if Core.file_exists(file):
				if "not touch" in file or "ser":
					self.conn.send(b"cant edit that file")
				else:
					fm.write_file(file, data=data)
					self.conn.send(b"wrote file")

		def writeJSON(self, data):
			data, file = data.split("/")
			jsData = Core.dataTypes.strDict(data)
			if Core.file_exists(file):
				if "no touch" in file:
					fm.write_json(jsData)

		def process(self, opCode, data):
			func = Core.switch(self.opCodeDict, opCode)
			func(data)

	"""
	Ran on server side
	"""
	class server:
		def __init__(self, host, port):
			self.ServerSocket = socket.socket()
			self.config = fm.getData_json("no_touch/config.json")
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
				uData = Core.dataTypes.strList(uData)
			elif 'dict' in dType:
				uData = Core.dataTypes.strDict(uData)
			elif 'str' in dType:
				uData = str(uData)
			elif 'float' in dType:
				uData = float(uData)
			elif 'int' in dType:
				uData = int(uData)
			elif 'bool' in dType:
				uData = bool(uData)

			actClass.process(opCode, uData)

		def threaded_client(self, connection, addr, c, actionsClass):
			SA = actionsClass(connection, addr, c, self.config)
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
			del conns[connection]
			connection.close()

		def main(self, actionsClass):
			while True:
				Client, address = self.ServerSocket.accept()
				print('Connected to: ' + address[0] + ':' + str(address[1]))
				start_new_thread(self.threaded_client, (Client, address, self.ThreadCount, actionsClass, ))
				self.ThreadCount += 1
				print('Thread Number: ' + str(self.ThreadCount))
			# break
			self.ServerSocket.close()