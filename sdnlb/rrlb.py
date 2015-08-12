from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import mac_learner
#from pox.lib.addresses import IPAddr
from pyretic.lib.query import *

class rrlb(DynamicPolicy):
	def __init__(self, switch, ips, macs,ports):
		super(rrlb, self).__init__()
		print "rrln creation!"
		self.switch = switch
		self.ips = ips
		self.macs = macs
		self.ports = ports
		self.ip = self.ips[0]
		self.mac = self.macs[0]
		self.client = 0
		Q = packets(limit=1, group_by=['srcip','srcport'])
		Q.register_callback(self.round_robin)
		self.policy = Q

	def round_robin(self, pkt):
		print "round_robin"
		print str(pkt)
		print str(pkt['switch'])
		print str(pkt['ethtype'])+" .. "+str(self.ip)
		dst_01 = match(srcip=pkt['srcip'], dstip=IPAddr('10.0.0.2'))


		flag = True
		for i in self.ips:
			if flag:
				srvs_src = match(srcip=i, dstip=pkt['srcip'])
				flag = False
			else:
				srvs_src = srvs_src | match(srcip=i, dstip=pkt['srcip'])
		other_switches = ~match(switch=self.switch)
		self.policy = if_(other_switches, identity, \
						if_(dst_01, modify(dstip=self.ip,dstmac=self.mac), \
							if_(srvs_src, modify(srcip=IPAddr('10.0.0.2'),srcmac=EthAddr("00:00:00:00:00:02")), \
							#if_(srvs_src, modify(srcip=IPAddr('10.0.0.2')), \
								self.policy)))
		self.client += 1
		self.ip = self.ips[self.client % len(self.ips)]
		self.mac = self.macs[self.client % len(self.macs)]

		print self.policy


def main():
	print "load balancer"
	#ips = [IPAddr('10.0.0.1'),IPAddr('10.0.0.2'),IPAddr('10.0.0.3')]
	ips = [IPAddr('10.0.0.3'),IPAddr('10.0.0.4')]
	#macs = [EthAddr("00:00:00:00:00:01"),EthAddr("00:00:00:00:00:02"),EthAddr("00:00:00:00:00:03")]
	macs = [EthAddr("00:00:00:00:00:03"),EthAddr("00:00:00:00:00:04")]
	ports = [10000,11000]

	rrlb_on_switch = rrlb(2,ips,macs,ports)

	forwardARP = match(ethtype=0x0806)
	forwardICMP = match(ethtype=0x0800,protocol=1)
	return if_(forwardICMP | forwardARP, mac_learner(), \
			rrlb_on_switch>>mac_learner())
#	return mac_learner()
