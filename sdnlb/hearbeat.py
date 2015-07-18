from soccketconnection import SocketConnection
from json_message import JsonMessage

class HeartBeat (object):

	def __init__(self,services,sendEvent=False):
		self.services = services
		self.sendEvent = sendEvent

	def start(self, queue):
		# start event listener
		p1 = Process(target=self.main)
		p1.start()

	def main(self):
		self.hearBeat()
		
		if (self.sendEvent):
			self.eventBeat()

	def heartBeat(self):
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

	def eventBeat(self):
		for (service in services):
			for server in service.server:
				socket = Socket()

				try:
					socket.connect(server.getIp(),server.getEventPort())
					socket.send(JsonMessage.genLoadMessage())
				except Exception,e
					# cannot connect with server
					server.setStatus(False)
