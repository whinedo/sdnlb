from soccketconnection import SocketConnection

class HeartBeat (object):

	def __init__(self,services):
		self.services = services


	def SimpleHeartBeat(self):
		for (service in services):
			for server in service.server:
				socket = Socket()

				try:
					socket.connect(server.getIp(),server.getPort())
				except Exception,e
					# cannot connect with server
					server.setStatus(False)
				finally:
					socket.close()

	def CpuHeartBeat(self):
		for (service in services):
			for server in service.server:
				socket = Socket()

				try:
					socket.connect(server.getIp(),server.getPort())
					socket.send("cpu")
				except Exception,e
					# cannot connect with server
					server.setStatus(False)
