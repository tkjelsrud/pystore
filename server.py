from threading import Timer

import socket
import select
import hashlib
import math

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
	cid = 0
	recv = []
	send = []
	
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

	def serve():
		
		try:
			serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			serverSocket.setblocking(0)
			serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			serverSocket.bind((self.host, self.port))
			serverSocket.listen(3)
		
			print "INFO: I am listening at %s" % (str(serverSocket.getsockname()))
			print "* I am ready to chat with a new client! *\n"
		
		except (socket.error, socket.gaierror) as err:
			print "\nERROR: Something went wrong in creating the listening socket:", err
			exit(1)
		try:
			while True:
				serverSocket.setblocking(False)
				readyForRecv, readyForSend = runSelect()
		
				for fd in readyForRecv:
					if fd == serverSocket:
						handleListeningSocket()
					else:
						handleConnectedSocket()
		
				"""for fd in readyForSend:
		try:
		    if fd in clientMessages.keys():  # See if connection information exists
		        broadcast = str(clientMessages[fd])  # Add message to broadcast variable
		
		    if broadcast:  # See if a message is actually there
		        for client in readyForSend:  # Broadcast message to every connected client
		            if broadcast != "":
		                print "* Broadcasting message \"%s\" to %s *" % (str(broadcast), client.getpeername())
		                client.send(str(fd.getpeername()) + ": " + str(broadcast))
		
		        clientMessages[fd] = ""  # Empty pending messages
		        """
		except:
			print "\nERROR: Something awful happened while broadcasting messages"
			break
		
			except socket.error as err:
			print "\nERROR: Something awful happened with a connected socket:", err
		
		"""if fd in recvList:
		recvList.remove(fd)
		
		if fd in sendList:
		sendList.remove(fd)
		
		fd.close()
		
		except KeyboardInterrupt:
		for fd in recvList:
		fd.close()
		
		for fd in sendList:
		fd.close()
		
		print "\nINFO: KeyboardInterrupt"
		print "* Closing all sockets and exiting... Goodbye! *"
		exit(0)		"""


	def connectSocket():
		try:
			sock, addr = serverSocket.accept()
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    		#sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    		#sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    		#sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)
		except socket.error as err:
			print "\nERROR: Something went wrong in the accept() function call:", err
			exit(1)
	
		try:
			#c = Client(cid++, sock, adr)
			# Keep connection open
			None
			#recvList.append(newConnectionSocket)
			#sendList.append(newConnectionSocket)
			#print "INFO: Connecting socket created between %s and %s" % (newConnectionSocket.getsockname(), newConnectionSocket.getpeername())
			#print "* Client %s is ready to chat *" % (str(newConnectionSocket.getpeername()))
		except (socket.error, socket.gaierror) as err:
			print "\nERROR: Something went wrong with the new connection socket:", err
			if c:
				# Something
				c.close()
			sock.close()
	
	def set(key, value, meta = None):
		# set some value
		None
	
	def tick():
		# Do cleanup and whatnot
		# Send pings/keepalive to clients?
		None

if __name__ == "__main__":
    HOST, PORT = "localhost", 8000
    
    server = TcpStorageServer(HOST, PORT)
    server.serve()

    # Create the server, binding to localhost on port 9999
    #server = SocketServer.TCPServer((HOST, PORT), TcpStorageServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    #server.serve_forever()