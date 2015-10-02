from heartbeat import HeartBeat
import time
from data_structures.services_proxy import ServicesProxy
from data_structures.parser import Parser
from socketconnection import SocketConnection
from json_message import *
import sdnlb_conf
import subprocess

def main():

    ip = "127.0.0.1"
    eventPort = 9000

    socket = SocketConnection()
    try:
    	socket.connect(ip,int(eventPort),60)
	cmd = "iperf"
	msg = JsonMessage.genCmdReqMessage(cmd)
	socket.send(msg)
    	msg = socket.receive()
    	
    	if msg != '':
    		(msgtype, data) = JsonMessage.parse_json(msg)
                print "MSG",msg
		
		if (msgtype == msgTypes['cmd_ans']):
			if (data['cmd'] == "iperf"):
				port = int(data['args'])
				time.sleep(2) # wait for iperf to start running	
				cmd = "iperf3"
                                args = "-c %s"%(ip)
				opts = "-t %d -p %d -J"%(int(sdnlb_conf.iperf_tout),int(port))
                		status = 0
                		output = subprocess.check_output([cmd, args,opts])
                                print output
                                
		                json_msg = JsonMessage.parse_iperf_json
                                print json_msg['start']
			
    except Exception,e:
    	# cannot connect with server
        print "Exception"
    	print e
    	#print "STATUS DOWN"
    finally:
    	socket.close()

	
if __name__ == "__main__":
	main()
