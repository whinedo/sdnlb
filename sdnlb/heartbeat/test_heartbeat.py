from heartbeat import HeartBeat
import time
from data_structures.services_proxy import ServicesProxy
from data_structures.parser import Parser
from socketconnection import SocketConnection
from json_message import *
import sdnlb_conf
from subprocess import Popen, PIPE, STDOUT
import logging

def main():

    ip = "127.0.0.1"
    eventPort = 9000
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("hb")

    socket = SocketConnection()
    try:
	socket.connect(ip,int(eventPort),10)
	cmd = "iperf"
	msg = JsonMessage.genCmdReqMessage(cmd)
	socket.send(msg)
	logger.debug("HB : sent:%s",msg)
    	msg = socket.receive()
    	
    	if msg != '':
    		(msgtype, data) = JsonMessage.parse_json(msg)
                print "MSG",msg
		
		if (msgtype == msgTypes['cmd_ans']):
			if (data['cmd'] == "iperf"):
				port = int(data['args'])
				time.sleep(4) # wait for iperf to start running	
                                cmd = 'iperf3 -c %s -t %d -p %d -J'%(ip,int(sdnlb_conf.iperf_tout),int(port))

                                p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                                output = p.stdout.read()

                                
                                print output

		                json_msg = JsonMessage.parse_iperf_json(output)
                                print json_msg['end']['cpu_utilization_percent']['remote_system']
			
    except Exception,e:
        print "Exception"
    	print e
    finally:
    	socket.close()

	
if __name__ == "__main__":
	main()
