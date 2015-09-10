import socket
import sdnlb_conf

class SocketConnection (object):

	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.settimeout(sdnlb_conf.socket_timeout)
		else:
			self.sock = sock
	
	def connect(self, host, port):
		self.sock.connect((host, port))
	
	def close(self):
		self.sock.close()

        def shutdown(self):
		self.sock.shutdown()
	
	def send(self, msg):
		totalsent = 0
		
		while totalsent < MSGLEN:
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent
	
	def receive(self):
	
		chunks = []
		bytesRecv = 0
	
		while bytes_recd < MSGLEN:
			chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
			if chunk == '':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytesRecv = bytesRecv + len(chunk)
	
		return ''.join(chunks)
