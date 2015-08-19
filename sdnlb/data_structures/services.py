from service import Service

class Services(object):

	def __init__(self):
		self.services = []

	def addService(self,service):
		self.services.append(service)

	def getServices(self):
		return self.services

	def setServer(self,lbPort,index,server):

		srvIdx = self.getServiceIndex(lbPort)

		if srvIdx != -1:
			service = self.getService(srvIdx)

			if (index > (len(service.getServers())-1) or index < 0):
				return -1

			else:
				service.setServer(index,server)	

	def setServerByIP(self,lbPort,ip,server):
		srvIdx = self.getServiceIndex(lbPort)

		if srvIdx != -1:
			service = self.getService(srvIdx)
			servers = service.getServers()
			index = None
			for i in range(len(servers)):
				if (servers[i].getIp()==ip):
					index = i

			if index != None:
				self.setServer(lbPort,index,server)

		


	def initializeServers(self):
		for i in range(len(self.services)):
			service = self.services[i]
			service.initializeServers()
			#self.setService(i,service)	#TODO CHECK this

	def getService(self,index):
		if (index > (len(self.services)-1)):
			return None

		elif (index < 0):
			return None
		else:
		 	return self.services[index]

	def setService(self,index,service):
		if (index < (len(self.services)) and index >= 0):
			self.services[index] = service
			

	def getServiceIndex(self,lbPort):
		for i in range(len(self.services)):
			service = self.services[i]
			
			if (int(service.getLbPort()) == lbPort):
				return i
	
		return -1

	def getPorts(self):
		ports = []

		for service in self.services:
			ports.append(int(service.getLbPort()))

		return ports

	def getServiceIps(self,lbport):
		ips = []
		serviceIndex = self.getServiceIndex(lbport)
		
		service = self.services[serviceIndex]
		for server in service.getServers():
			ips.append(server.getIp())
