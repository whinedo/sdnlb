import re
from services import Services
from service import Service
from server import Server

class Parser:

	def __init__(self,configFile):
		self.configFile = configFile
		self.weightRe = re.compile('(\d+) (\w+) (\d+) (\d+)')
		self.noWeightRe = re.compile('(\d+) (\w+) (\d+)')


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
			weightReRes = self.weightRe.match(line)
			noWeightReRes = self.noWeightRe.match(line)
			lbPort = None
			ip = None
			port = None
			weight = None
			status = False
			
			if (weightReRes != None):
				lbPort = weightReRes.group(1)	
				ip = weightReRes.group(2)	
				port = weightReRes.group(3)	
				weight = weightReRes.group(4)	

			elif (weightReRes != None):
				lbPort = weightReRes.group(1)	
				ip = weightReRes.group(2)	
				port = weightReRes.group(3)

			else:
				continue

			index = services.getServiceIndex()

			if (index == -1):
				#new service
				service = Service(lbPort)
			else:
				service = services.getService(index)

			services.append(service)
			service.addServer(Server(ip,port,status,weight))

		return services
