from ilbagorithm import LBAlgorithm
import sdnlb_conf


class LeastConnections(LBAlgorithm):
	def getServer(self,services,service):
		servers = service.getServers()
		server = None

		for i in range(len(servers)):
			index = self.getLeastConnectionsServer(service)
			if index != None: 
				server_aux = service.getServer(index)
				print "------------------------"
				print "SERVICE MIN CONS SRV:%d ip:%s"%(index,server_aux.getIp())
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


	def getLeastConnectionsServer(self,service):
		minConn = sdnlb_conf.max_conns
		servers = service.getServers()
		index = None

		for i in range(len(servers)):
			server = servers[i]

                        #DEBUG
                        print "index:%d CONS:%d"%(i,server.getConnections())
                        #FINDEBUG

			if (server.getConnections() <= minConn and server.getStatus() == True):
                                minConn = server.getConnections()
				index = i

                #DEBUG
                if index != None:
                        print "Min index:%d CONS:%d"%(index,servers[index].getConnections())
                #FINDEBUG
		return index
				

