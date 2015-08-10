from multiprocessing import Process
import time
from socketconnection import SocketConnection
from json_message import JsonMessage
import sdnlb_conf

class HeartBeat (object):

	def __init__(self,ip,services,sendEvent=False):
		self.services = services
		self.sendEvent = sendEvent
		self.timeout = sdnlb_conf.hb_timeout
		self.ip = ip

	def getIp(self):
		return self.ip

	def start(self):
		# start event listener
		p1 = Process(target=self.main)
		p1.start()

	def main(self):
		while True:
			self.heartBeat()
			
			if (self.sendEvent):
				self.eventBeat()

			time.sleep(self.timeout)

	def heartBeat(self):
		for service in self.services.getServices():
			for server in service.getServers():

				socket = SocketConnection()

				try:
					socket.connect(server.getIp(),server.getPort())
					print "STATUS OK"
					server.setStatus(True)
				except Exception,e:
					# cannot connect with server
					#print e
					#print "STATUS DOWN"
					server.setStatus(False)
				finally:
					socket.close()

	def eventBeat(self):
		for service in self.services:
			for server in service.getServers():
				socket = Socket()

				try:
					socket.connect(server.getIp(),server.getEventPort())
					socket.send(JsonMessage.genLoadMessage())
				except Exception,e:
					# cannot connect with server
					server.setStatus(False)
