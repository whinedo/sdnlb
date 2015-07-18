class Server (object):
	
	def __init__(self,ip,port,status,weight):
		self.ip = ip
		self.port = port
		self.status = status
		self.weigth = weigth


	def getIp(self):
		return self.ip

	def setIp(self,ip):
		self.ip = ip

	
	def getPort(self):
		return self.port

	def setPort(self,port):
		self.port = port

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


