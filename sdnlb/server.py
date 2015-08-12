class Server (object):
	
	def __init__(self,ip,mac,port,status,eventPort,weight):
		self.ip = ip
		self.mac = mac
		self.port = int(port)
		self.eventPort = eventPort
		self.status = status
		self.weight = weight
		self.connections = -1
		self.cpu = -1


	def getIp(self):
		return self.ip

	def setIp(self,ip):
		self.ip = ip

	def getMac(self):
		return self.mac

	def setMac(self,mac):
		self.mac = mac

	
	def getPort(self):
		return self.port

	def setPort(self,port):
		self.port = port

	def getEventPort(self):
		return self.eventPort

	def setEventPort(self,eventPort):
		self.eventPort = eventPort

	def getStatus(self):
		return self.status

	def setStatus(self,status):
		self.status = status

	def isActive(self):
		return self.getStatus() == True

	
	def getWeight(self):
		return self.weight

	def setWeight(self,weight):
		self.weight = weight


	def getConnections(self):
		return self.connections

	def setConnections(self,connections):
		self.connections = connections


	def getCpu(self):
		return self.cpu

	def setCpu(self,cpu):
		self.cpu = cpu


