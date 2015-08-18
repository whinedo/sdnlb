from abc import ABCMeta, abstractmethod

class LBAlgorithm(object):
        __metaclass__ = ABCMeta

	@abstractmethod
	def getServer(self,services,service):
		pass
