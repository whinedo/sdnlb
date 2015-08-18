from ilbagorithm import LBAlgorithm
import random

class WeightRoundRobin(LBAlgorithm):
	def getServer(self,services,service):
		service.incrementLastSrv()
		servers = service.getServers()
		server = None

		for i in range(len(servers)):
			server_aux = service.getServer(service.getLastSrv())
			print "------------------------"
			print "SERVICE LAST SRV:",service.getLastSrv()
			print "STATUS:",server_aux.getStatus()
			print "------------------------"
			if (server_aux.getStatus() == True):
				r = random.random()
				ci = float(server.getData())
				
				if (r <= ci):
					server = server_aux
					print "------------------------"
					print "SERVER FOUND"
					print "------------------------"
					break
			else:
				service.incrementLastSrv()


		# service must be set again by services proxy in order to be updated in Manager
		serviceIdx = services.getServiceIndex(service.getLbPort())
		services.setService(serviceIdx,service)

		#DEBUG
		print "round_robin"
		service = self.services.getService(serviceIdx)
		print "service last srv after set:",service.getLastSrv()
		#FINDEBUG

		return server

