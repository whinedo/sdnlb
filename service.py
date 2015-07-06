class Service:
	def __init__(self,lbPort):
		self.last_srv = -1
		self.lbPort = lbPort
		self.servers = []


	def addServer(self,server):
		self.servers.append(server)

	def getServer(self,index):
		if (index > (len(self.server)-1)):
			return None

		elif (index < 0):
			return None
		else
		 	return self.servers[index]

	def getLbPort(self):
		return self.lbPort
