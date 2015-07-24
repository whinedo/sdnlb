from parser import Parser
from pyretic.core import packet
from pyretic.lib.corelib import *
from pyretic.lib.query import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import mac_learner
from utils_packet import *
    
#class RRlb(object):
class RRlb(DynamicPolicy):
	def __init__(self,services):
		super(RRlb, self).__init__()

		self.services = services

		#Q = packets(limit=1,group_by=['srcip'])
		Q = packets(limit=1,group_by=['srcip','srcport'])

		Q.register_callback(self.round_robin)
		#self.policy = match(dstport=80) >> Q
		self.policy = Q
		self.policy = flood() + self.policy

		#DEBUG
		self.server = self.services.getService(0).getServer(0)
		#FINDEBUG

	def round_robin(self,pkt):
		#print pkt['srcport']
		#srcport = pkt['srcport']

		print "ethtype:",pkt['ethtype']
#		getTcpPorts(pkt)		
	
		#DEBUG
		dstPort = 10000
		#FINDEBUG
	
		#self.policy = if_(match(srcip="10.0.0.100"),
		self.policy = if_(match(srcip=pkt['srcip'],dstip='10.0.0.100',dstport=pkt['dstport'],ethtype=packet.IPV4, protocol=packet.TCP_PROTO),
				modify(dstip=self.server.getIp()),
				self.policy)
	
	
		print dir(pkt)
		
		serviceIndex = self.services.getServiceIndex(dstPort)
		print ".............."
	
		print serviceIndex
		service = self.services.getService(serviceIndex)
		service.incrementLastSrv()
	
		#self.server = self.servers[self.client % m]
	
		#DEBUG
		self.server = self.services.getService(serviceIndex).getServer(0)
		print self.server
		#FINDEBUG

def genDynRules():
	return RRlb(services) >> mac_learner()

def staticFilterServices():
	parser = Parser('/home/mininet/sdnlb/sdnlb/sdnlb.conf')
	services = parser.parse()

	mtch = None
	for service in services:
		mtch = 

def staticFilterTcp():
	return if_(match(ethtype=packet.IPV4, protocol=packet.TCP_PROTO),genDynRules(),mac_learner())
    
def main():
	#return dynamic(RRlb) () >> forward #TODO debe completarse con los parentesis finales
	#return dynamic(RRlb)() >> dynamic(learn)()
	sip = "10.0.0.100"
	
	#return match(ethtype=packet.IPV4, protocol=packet.TCP_PROTO) >> RRlb() >> mac_learner()
	return staticFilterTcp()
