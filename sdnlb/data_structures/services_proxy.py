from multiprocessing.managers import BaseProxy
from services import *

class ServicesProxy(BaseProxy):

	def addService(self,service):
		return self._callmethod('addService', [service])

	def getService(self,index):
		return self._callmethod('getService', [index])

	def getServices(self):
		return self._callmethod('getServices')

	def getServiceIndex(self,lbPort):
		return self._callmethod('getServiceIndex', [lbPort])

	def setServer(self,lbPort,server,index=None,ip=None):
		if index != None:
			return self._callmethod('setServer', [lbPort,index,server])
		elif ip != None:
			return self._callmethod('setServerByIP', [lbPort,ip,server])

	def getServer(self,lbPort,index):
		return self._callmethod('getServer', [lbPort,index])

	def getPorts(self):
		return self._callmethod('getPorts')

	def getServiceIps(self,lbPort):
		return self._callmethod('getServiceIps', [lbPort])

	def setService(self,index,service):
		return self._callmethod('setService', [index,service])

	def initializeServers(self):
		return self._callmethod('initializeServers', [])
