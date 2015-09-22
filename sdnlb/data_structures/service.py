from sets import Set

class Service (object):
	def __init__(self,lbPort):
		self.last_srv = -1
		self.lbPort = lbPort
		self.servers = []
		self.maxWeight = 0

	def initializeServers(self):
                self.setMaxWeight()
		for server in self.servers:
			weight = server.getWeight()
			try:
				server.setData(float(weight)/float(self.maxWeight))
			except ZeroDivisionError,e:
			 	pass

	def setMaxWeight(self):
		for server in self.servers:
			weight = server.getWeight()
			if weight > 0 and weight > self.maxWeight:
				self.maxWeight = weight
	
	def getServers(self):
		return self.servers

	def addServer(self,server):
		self.servers.append(server)

	def getServer(self,index):
		if (index > (len(self.servers)-1)):
			return None

		elif (index < 0):
			return None
		else:
		 	return self.servers[index]

	def setServer(self,index,server):
		
		if (index < (len(self.servers)) and index >= 0):
		 	self.servers[index] = server

		#print "index",index
		#print self.servers[index].printAll()
		#print self.servers[index].getStatus()

	
	def getLastSrv(self):
		return self.last_srv

	def getLbPort(self):
		return self.lbPort

        def getEventPorts(self):
                portsSet = Set()

                for server in self.servers:
                    eventPort = server.getEventPort()
                    portsSet.add(eventPort)
                return portsSet

	def incrementLastSrv(self):
		self.last_srv = (self.last_srv + 1) % len(self.servers)
		print "LAST SRV incremented:",self.last_srv
