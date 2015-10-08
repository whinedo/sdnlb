from ilbagorithm import LBAlgorithm

class LeastLoad(LBAlgorithm):
	def getServer(self,services,service):
		servers = service.getServers()
		server = None

		for i in range(len(servers)):
			index = self.getLeastCpuLoadServer(service)
			if index != None: 
				server_aux = service.getServer(service.getLastSrv())
				print "------------------------"
				print "SERVICE LAST SRV:",service.getLastSrv()
				print "STATUS:",server_aux.getStatus()
				print "------------------------"
				server = server_aux
				
		# service must be set again by services proxy in order to be updated in Manager
#		serviceIdx = services.getServiceIndex(service.getLbPort())
#		services.setService(serviceIdx,service)
#
#		#DEBUG
#		print "round_robin"
#		service = self.services.getService(serviceIdx)
#		print "service last srv after set:",service.getLastSrv()
#		#FINDEBUG

		return server


	def getLeastCpuLoadServer(self,service):
		minCpu = servers[0].getCpu()
		servers = service.getServers()
		index = None

		for i in range(len(servers)):
			server = servers[i]

			if (server.getCpu() <= minCpu and server.getStatus() == True):
				index = i
				break

		return index
				

