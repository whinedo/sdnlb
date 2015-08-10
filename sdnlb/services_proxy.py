from services import *

class ServicesProxy(multiprocessing.managers.Base):

	def addService(self,service):
		return self._callmethod('addService', [service])

	def getServices(self):
		return self._callmethod('getServices')

	def getServiceIndex(self,lbPort):
		return self._callmethod('getServiceIndex', [lbPort])

	def getPorts(self):
		return self._callmethod('getPorts')

	def getServiceIps(self,lbport):
		return self._callmethod('getServiceIps', [lbPort])
