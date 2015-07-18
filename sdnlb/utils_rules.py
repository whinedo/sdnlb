from pyretic.lib.corelib import *
from pyretic.lib.std import *

def subs(c,cp,r,rp,p,pp):
	"""from client, substitute replica address for the public address 
	from server, substitute public address for replica address and ports"""
	
	#c: client, cp: client port, r: replica, rp:replica port, p: public address, pp:public port
	    
	c_to_p = match(srcip=c,dstip=p,srcport=cp,dstport=pp, ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
	r_to_c = match(srcip=r,dstip=c,srcport=rp,dstport=cp, ethtype=packet.IPV4, protocol=packet.TCP_PROTO)

	return ((c_to_p & modify(dstip=r,dtsport=rp)) + 
	        (r_to_c & modify(srcip=p,srcport=pp)) + 
	        (~r_to_c & ~c_to_p))

def rewrite(c,cp,r,rp,p,pp):
	#c: client, cp: client port, r: replica, rp:replica port, p: public address, pp:public port
	return subs(c,cp,r,rp,p,pp)

