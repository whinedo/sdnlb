from service import Service

class Services:

	def __init__(self):
		self.services = []

	def addService(self,service):
		self.services.append(service)

	def getService(self,index):
		if (index > (len(self.services)-1)):
			return None

		elif (index < 0):
			return None
		else:
		 	return self.services[index]

	def getServiceIndex(self,lbPort):
		for i in range(len(self.services)):
			service = self.services[i]

			if (service.getLbPort() == lbPort):
				return i
	
		return -1

