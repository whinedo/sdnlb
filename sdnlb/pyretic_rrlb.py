from parser import Parser
from pyretic.core import packet
from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import learn

    
#class RRlb(object):
class RRlb(DynamicPolicy):
	def __init__(self):
		super(RRlb, self).__init__()

		parser = Parser('/home/mininet/sdnlb/sdnlb/sdnlb.conf')
		self.services = parser.parse()

		#Q = packets(limit=1,group_by=['srcip'])
		Q = packets(limit=1,group_by=['dstip'])

		Q.register_callback(self.round_robin)
		#self.policy = match(dstport=80) >> Q
		self.policy = Q

		#DEBUG
		self.server = self.services.getService(0).getServer(0)
		#FINDEBUG

	def round_robin(self,pkt):

		#self.policy = if_(match(srcip="10.0.0.100"),
		self.policy = if_(match(srcip=pkt['srcip'],dstip='10.0.0.100',ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
				modify(dstip=self.server.getIp()),
				self.policy)

		print pkt
		print pkt['srcport']
		serviceIndex = self.services.getServiceIndex(pkt['srcport'])
		print ".............."

		print serviceIndex
		self.service = self.services.getService(serviceIndex)
		self.service.incrementLastSrv()

		#self.server = self.servers[self.client % m]

		#DEBUG
		self.server = self.services.getService(serviceIndex).getServer(0)
		print self.server
		#FINDEBUG
    
def main():
	#return dynamic(RRlb) () >> forward #TODO debe completarse con los parentesis finales
	#return dynamic(RRlb)() >> dynamic(learn)()
	return RRlb() >> dynamic(learn)()
