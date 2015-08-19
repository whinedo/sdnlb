from server import Server
from services import Services
from service import Service
import re

class Parser:

	def __init__(self,configFile):
		self.configFile = configFile
		self.commentRe = re.compile ('#+.*')
		self.weightRe = re.compile('(\d+) ([\w\.]+) (\d\d:\d\d:\d\d:\d\d:\d\d:\d\d) (\d+) (\d+) (\d+)')
		self.dynRe = re.compile('(\d+) (\w+) (\w+) (\d+) (\d+)')


	def parse(self):
		fd = None
		try:
			fd = open(self.configFile,"r")
			services = Services()

		except Exception,e:
			print "Cannot open config file:%s"%(self.configFile)
			return None

		lines = fd.readlines()

		for line in lines:
			line = line.replace("\n","")

			commentReRes = self.commentRe.match(line)
			dynReRes = self.dynRe.match(line)
			weightReRes = self.weightRe.match(line)

			lbPort = None
			ip = None
			mac = None
			port = None
			weight = None
			eventport = None
			status = False
			
			if (commentReRes != None):
				continue

			if (weightReRes != None):
				print line
				lbPort = int(weightReRes.group(1))
				ip = weightReRes.group(2)	
				mac = weightReRes.group(3)
				port = weightReRes.group(4)	
				eventPort = int(weightReRes.group(5))
				weight = weightReRes.group(6)	

			elif (dynReRes != None):
				print line
				lbPort = int(dynReRes.group(1))
				ip = dynReRes.group(2)	
				mac = weightReRes.group(3)
				port = int(dynReRes.group(4))
				eventPort = dynReRes.group(5)	

			else:
				continue

			index = services.getServiceIndex(lbPort)

			if (index == -1):
				#new service
				service = Service(lbPort)
				services.addService(service)
			else:
				service = services.getService(index)

			service.addServer(Server(ip,mac,port,status,eventPort,weight))

		return services
