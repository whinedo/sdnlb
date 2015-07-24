from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *


def getTcpPorts(pkt):
	print pkt
	print pkt.available_fields()
	print "ethtype:",pkt['ethtype']
	
	if pkt['ethtype'] == IP_TYPE:
		print "Ethernet packet, try to decode"
		raw_bytes = [ord(c) for c in pkt['raw']]
		print "ethernet payload is %d" % pkt['payload_len']    
		eth_payload_bytes = raw_bytes[pkt['header_len']:]   
		print "ethernet payload is %d bytes" % len(eth_payload_bytes)
		ip_version = (eth_payload_bytes[0] & 0b11110000) >> 4
		ihl = (eth_payload_bytes[0] & 0b00001111)
		ip_header_len = ihl * 4
		ip_payload_bytes = eth_payload_bytes[ip_header_len:]
		ip_proto = eth_payload_bytes[9]
		print "ip_version = %d" % ip_version
		print "ip_header_len = %d" % ip_header_len
		print "ip_proto = %d" % ip_proto
		print "ip payload is %d bytes" % len(ip_payload_bytes)
		if ip_proto == 0x06:
			print "TCP packet, try to decode"
			tcp_data_offset = (ip_payload_bytes[12] & 0b11110000) >> 4
			tcp_header_len = tcp_data_offset * 4
			print "tcp_header_len = %d" % tcp_header_len
			tcp_payload_bytes = ip_payload_bytes[tcp_header_len:]
			print "tcp payload is %d bytes" % len(tcp_payload_bytes)
			if len(tcp_payload_bytes) > 0:
				print "payload:\t",
				print ''.join([chr(d) for d in tcp_payload_bytes])


			tcp_src_port = (ip_payload_bytes[0] & 0xFFFF) << 16
			tcp_src_port |= (ip_payload_bytes[1] & 0xFFFF) 

			print "tcp_src_port :",tcp_src_port

			tcp_dst_port = (ip_payload_bytes[2] & 0xFFFF) << 16
			tcp_dst_port |= (ip_payload_bytes[3] & 0xFFFF) 

			print "tcp_dst_port :",tcp_dst_port
