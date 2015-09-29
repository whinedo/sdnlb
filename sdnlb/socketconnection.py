import socket
import sdnlb_conf

MSGLEN = 2048

class SocketConnection (object):

	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.settimeout(sdnlb_conf.socket_timeout)
		else:
			self.sock = sock
	
	def connect(self, host, port,timeout=None):
		if timeout != None:
			#DEBUG
			print "setting socket timeout:%d"%timeout
			#FINDEBUG
			self.sock.settimeout(timeout)

		self.sock.connect((host, port))
	
	def close(self):
		self.sock.close()

        def shutdown(self):
		self.sock.shutdown(socket.SHUT_RDWR)
	
	def send(self, msg):
		totalsent = 0
		
		while totalsent < len(msg):
			print msg[totalsent:]
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent
	
	def receive(self):
	
		chunks = []
		closed = False
	
		while not closed:
			chunk = self.sock.recv(2048)
			if chunk == '':
				closed = True
			chunks.append(chunk)
	
		return ''.join(chunks)
