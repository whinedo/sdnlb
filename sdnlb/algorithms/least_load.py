from ilbagorithm import LBAlgorithm

class LeastLoad(LBAlgorithm):
	def getServer(self,services,service):
		servers = service.getServers()
		server = None

		for i in range(len(servers)):
			index = self.getLeastCpuLoadServer(service)
			if index != None: 
				server_aux = service.getServer(index)
				#DEBUG
				print "------------------------"
				print "SERVICE MIN CPU SRV:%d ip:%s"%(index,server_aux.getIp())
				print "STATUS:",server_aux.getStatus()
				print "------------------------"
				#FINDEBUG
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
		servers = service.getServers()
		minCpu = 1
		index = None

		for i in range(len(servers)):
			server = servers[i]

                        #DEBUG
                        print "index:%d CPU:%f"%(i,server.getCpu())
                        #FINDEBUG
			if (server.getCpu() < minCpu and server.getStatus() == True):
				minCpu = server.getCpu()
				index = i

                #DEBUG
                if index != None:
                        print "Min index:%d CPU:%f"%(index,servers[index].getCpu())
                #FINDEBUG
		return index
				

