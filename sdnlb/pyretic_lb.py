from pyretic.core import packet
from pyretic.lib.corelib import *
from pyretic.lib.query import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import mac_learner
from utils_packet import *
import sdnlb_conf
from heartbeat.heartbeat import HeartBeat 
from data_structures.parser import Parser
from data_structures.mymanager import MyManager
#from services import Services
from data_structures.services_proxy import ServicesProxy
#from lb_algorithms import LBAlgorithms
from algorithms.factory import AlgoFactory

    
class LoadBalancer(DynamicPolicy):
	def __init__(self,switch,ip,mac,algo):
		super(LoadBalancer, self).__init__()

                self.algo = algo

		manager = MyManager()
		manager.register('setup_services',setup_services,proxytype=ServicesProxy)
    		manager.start()
		services_proxy = manager.setup_services()

		self.services = services_proxy
		self.switch = switch
		self.ip = ip
                self.mac = mac
		

		Q = packets(limit=1,group_by=['srcip','srcport','dstport'])

		Q.register_callback(self.loadBalancing)
		self.policy = Q


		self.hb = HeartBeat(sdnlb_conf.switch_ip,services_proxy,sdnlb_conf.event)
		self.hb.start()

		self.services.initializeServers()


	def genHbRules(self):

		hb_rl = None

	
		for service in self.services.getServices():
			servers = service.getServers()
			for i in range(len(servers)):

				server = servers[i]
				if i == 0:

					hb_rl = match(srcip=IPAddr(self.hb.getIp()), dstip=IPAddr(server.getIp()),dstport=server.getPort(), ethtype=packet.IPV4, protocol=packet.TCP_PROTO) | match(srcip=IPAddr(server.getIp()), dstip=IPAddr(self.hb.getIp()),srcport=server.getPort(), ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
				else:
					hb_rl |= match(srcip=IPAddr(self.hb.getIp()), dstip=IPAddr(server.getIp()),dstport=server.getPort(), ethtype=packet.IPV4, protocol=packet.TCP_PROTO) | match(srcip=IPAddr(server.getIp()), dstip=IPAddr(self.hb.getIp()),srcport=server.getPort(), ethtype=packet.IPV4, protocol=packet.TCP_PROTO)

		return hb_rl

	def genDstSrv(self,ports,ip,pkt):

		dst_srv_rl = None

		dst_srv_rl = match(srcip=pkt['srcip'], srcport=pkt['srcport'],dstip=IPAddr(ip),dstport=ports[0], ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
		
		if (len(ports) > 1):	
			for i in range(1,len(ports)):
				dst_srv_rl |= match(srcip=pkt['srcip'], srcport=pkt['srcport'], dstip=IPAddr(ip),dstport=ports[i], ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
			
		return dst_srv_rl


        def connecionForwardRules(self,pkt):
                #forward every packet with destination port not used by load balancing
                forwardRules = match(srcip=pkt['srcip'], srcport=pkt['srcport'],dstip=pkt['dstip'],dstport=pkt['dstport'], ethtype=packet.IPV4, protocol=packet.TCP_PROTO) | \
                             match(srcip=pkt['dstip'], srcport=pkt['dstport'],dstip=pkt['srcip'],dstport=pkt['srcport'], ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
                return forwardRules

                
	def loadBalancing(self,pkt):

		#DEBUG
		print "-----------------------------"
		print "PACKET:",pkt
		print "-----------------------------"
		#FINDEBUG

		other_switches = ~match(switch=self.switch)

		if (str(pkt['srcip']) == self.hb.getIp() or str(pkt['dstip']) == self.hb.getIp()):
			hb_rl = self.genHbRules()
			self.policy = if_(other_switches, identity, \
				if_(hb_rl, identity, self.policy))

		else:
	
			ports = self.services.getPorts()
	
			dstPort = int(pkt['dstport'])
	
			ips = self.services.getServiceIps(dstPort)
	
			serviceIndex = self.services.getServiceIndex(dstPort)

			if serviceIndex != -1:
				
				#DEBUG
				print "service index:",serviceIndex	
				#FINDEBUG
	
				service = self.services.getService(serviceIndex)
	
				#server = self.round_robin_algo(service)
                                if self.services != None:
                                    print "------------aaaaaaaa----------aaaaaaa-------"
				server = self.algo.getServer(self.services,service)
			
				if server != None:
	
					print ".............."
					print server
					print "service index:",serviceIndex	
					print ".............."
			
					#i = 1

					port = pkt['dstport']
					dst_srv = match(srcip=pkt['srcip'], dstip=IPAddr(self.ip),dstport=port, ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
					
				
					srvs_src = match(srcip=server.getIp(), dstip=pkt['srcip'],dstport=pkt['srcport'])
			
					other_switches = ~match(switch=self.switch)
					dst_srv = self.genDstSrv(ports,self.ip,pkt)
					hb_rl = self.genHbRules()
			
					self.policy = if_(other_switches, identity, \
								if_(dst_srv, modify(dstip=server.getIp(),dstmac=server.getMac()), \
									#if_(srvs_src, modify(srcip=IPAddr('10.0.0.2'),srcmac=EthAddr("00:00:00:00:00:02")), \
									if_(srvs_src, modify(srcip=IPAddr(self.ip),srcmac=EthAddr(self.mac)), \
										self.policy)))
                                        server.incrementConnections()
                                        self.services.setServer(service.getLbPort(),server,ip=server.getIp())
                                        # update server because connections attribute has been modified
					print self.policy

			else:
				#DEBUG
				print "SHITTTTTTT"
				#FINDEBUG
                                forwardRules = self.connecionForwardRules(pkt)

		        	self.policy = if_(forwardRules, identity,self.policy)
                                print self.policy
		
	
		
def staticFilterTcp():
	return if_(match(ethtype=packet.IPV4, protocol=packet.TCP_PROTO),genDynRules(),mac_learner())

def setup_services():
	parser = Parser('/home/mininet/sdnlb/sdnlb/servers.conf')
	services = parser.parse()
	return services
    
def main():

	algoType = sdnlb_conf.algo
	algo = AlgoFactory.getAlgoInstance(algoType)

	rrlb_sdn = LoadBalancer(sdnlb_conf.switch,sdnlb_conf.sip,sdnlb_conf.smac,algo)

	forwardARP = match(ethtype=0x0806)
	forwardICMP = match(ethtype=0x0800,protocol=1)
	return if_(forwardICMP | forwardARP, mac_learner(), \
			rrlb_sdn >>mac_learner())

