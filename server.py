from threading import Timer

import socket
import select
import hashlib
import math
import threading
import time
import os

def hello():
    print "hello, world"

#t = Timer(5.0, hello)
#t.start()  # after 30 seconds, "hello, world" will be printed

# Strategy, create 4 segments, different sizes depending on usage?
#
#
class Segment:
	HashSize = 2 # 2 byte = 16 bit = 65k elements 
	IDSize = 16 # 16 byte
	MetaSize = 16
	
	def __init__(self, dtSize = 512, master = True, distr = True):
		self.index = []
		self.dataSize = dtSize - Segment.MetaSize - Segment.IDSize
		self.master = master
		self.distr = distr
		self.frameSize = Segment.IDSize + Segment.MetaSize + self.dataSize
		self.alloc = int(math.pow(2, Segment.IDSize))
		self.data = bytearray(self.frameSize * self.alloc)
	
	def strToIdx(self, key):
		bt = hashlib.md5(key).digest()[0:Segment.HashSize]
		idx = ord(bt[0]) * ord(bt[1]) # noob
		return idx
		#md5(from key)
		#last 32 bytes (from key), if less
		#query the index at md5 loc and check match of key

	def strToIds(self, key):
		ids = key[Segment.IDSize * -1:]
		ids += b"\0" * (Segment.IDSize - len(ids))
		return ids
		
	def set(self, key, value):
		idx = self.strToIdx(key)
		ids = self.strToIds(key)
		payl = value[-self.frameSize:]
		payl += b"\x20" * (self.frameSize-Segment.IDSize - Segment.MetaSize - len(payl))
		data = bytearray(self.frameSize)
		data[0:Segment.IDSize] = ids
		data[Segment.IDSize + Segment.MetaSize:] = payl
		self.inject(idx, data)
		# COLLISION DETECTION
		
		
	def get(self, key):
		# use hash instead, get exact loc
		idx = self.strToIdx(key)
		ids = self.strToIds(key)
		
		bt = self.data[idx:idx + Segment.IDSize]
		
		if bt == ids:
			# Element found, and ID match
			return self.extract(idx)
		
		return False

	def inject(self, idx, data):
		if len(data) != self.frameSize:
			raise Exception('inject', 'illegal size of data=' + str(len(data)))
		self.data[idx:idx+self.frameSize] = data

	def extract(self, idx):
		bt = self.data[idx:idx+self.frameSize]
		return (bt[0:Segment.IDSize], 
			bt[Segment.IDSize : Segment.IDSize+Segment.MetaSize], 
			bt[Segment.IDSize+Segment.MetaSize : self.frameSize])
	
	def Store():
		# Store segment to non-volatile media
		# lock index
		# store
		# unlock and/or fail
		None


class Que:
	#
	None
	
class Client:
	# Client
	def __init__(self, cid, socket, address):
		self.cid = cid
		self.socket = socket
		self.address = address
		self.rQue = []
		self.wQue = []
		self.active = True
	
class OtherServer(Client):
	#
	None

class TcpStorageServer:
	# define 
	cid = 0
	
	otherServers = {}
	segments = {}
	config = {}

	def __init__(self, host, port):
		self.cid = 0
		self.connections = {}
		self.host = host
		self.port = port
		
		# Init with a store
		self.segments[0] = Segment()
		self.segments[0].set("test", "testverdi her123!")
		self.segments[0].set("hallo", "hei pa deg")

	def serve(self):
		
		try:
			serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#serverSocket.setblocking(0)
			#serverSocket.settimeout(10)
			serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			serverSocket.bind((self.host, self.port)) #socket.gethostname()
			serverSocket.listen(5)
		
			print "INFO: SERVING %s" % (str(serverSocket.getsockname()))
		
		except (socket.error, socket.gaierror) as err:
			print "\nERROR: Something went wrong in creating the listening socket:", err
			exit(1)

		while True:
			client = None
			cid = None
			try:
				(client, address) = serverSocket.accept()
				#lock()
				cid = self.newClient(client, address)
				client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
				
				tR = threading.Thread(target = self.readSocket,args = (client, cid))
				tR.setDaemon(True)
				tR.start()
				tW = threading.Thread(target = self.writeSocket,args = (client, cid))
				tW.setDaemon(True)
				tW.start()
			except Exception as err:
				#unlock
				if cid:
					self.connections[cid].active = False
				if client:
					client.close()
				print("Failed during client connect", err.strerror)
				break

	def newClient(self, client, address):
		try:
			cid = self.cid + 1
			self.cid = cid
			c = Client(cid, client, address)
			self.connections[cid] = c
			return cid
		except Exception as err:
				print("Failed to create client", err.strerror)
		return None

	def readSocket(self, client, cid):
		size = 1024
		try:
			while True:
				data = client.recv(size)
				#
				# Use first two bytes for command and segment ID?
				#
				cmd = data[0:2]
				sid = data[2:4]
				print("CMD", cmd)
				print("ID ", sid)
				print(str(len(data)) + ": " + data)
				
				if cmd == "GE":
				    s = self.segments[int(sid)]
				    key = str(data[4:]).strip()
				    print("GEt key", key)
				    
				    dx = s.get(key)
				    print(str(dx))
				    
				    self.connections[cid].wQue.append(dx[2])
				
				#if cmd == "SE":
				#    s = self.segments[int(sid)]
				#    key = str(data[4:]).strip()
				    
				else:
				    self.connections[cid].rQue.append(data)
				    self.connections[cid].wQue.append(str(len(data)) + ": " + data)
				time.sleep(0.100)
		except Exception as err:
			print("Failed during client read", err)
			client.close()
	
	def writeSocket(self, client, cid):
		try:
			while True:
				while len(self.connections[cid].wQue) > 0:
					client.send(self.connections[cid].wQue.pop())
				time.sleep(0.100)
		except Exception as err:
			print("Failed during client connect", err)
			client.close()
	
	def set(key, value, meta = None):
		# set some value
		None
	
	def tick():
		# Do cleanup and whatnot
		# Send pings/keepalive to clients?
		None

if __name__ == "__main__":
    HOST, PORT = "localhost", int(os.environ.get('PORT', 8000)) #"localhost"  socket.gethostname(),
    
    try:
        server = TcpStorageServer(HOST, PORT)
        
    	server.serve()
    except:
    	print("Exit")

	print(threading.enumerate())

    # Create the server, binding to localhost on port 9999
    #server = SocketServer.TCPServer((HOST, PORT), TcpStorageServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    #server.serve_forever()
