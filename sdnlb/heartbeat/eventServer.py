#!/usr/bin/env python
import multiprocessing
import time
import socket
from json_message import *
import logging
import sys,re
import subprocess
from subprocess import Popen, PIPE, STDOUT
import psutil
import sdnlb_conf

 
class Server (object):

	def __init__(self, hostname, port):

                logging.basicConfig(filename='log/event.log', level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S %p')
                self.logger = logging.getLogger('event')
		self.hostname = hostname
		self.port = port
	
	def start(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.hostname, self.port))
		self.socket.listen(1)
		self.logger.info("listening on port:%d"%self.port)
	
		while True:
			conn, address = self.socket.accept()
			self.logger.debug("New connection")
			process = multiprocessing.Process(target=self.handle, args=(conn, address,self.port))
			process.daemon = True
			process.start()
			self.logger.debug("Started process %r", process)


	def getConnections(self,port):
                #cmd = "netstat -anpt | grep %s:%d | grep ESTABLISHED | wc -l"%(ip,port)
                cmd = "netstat -anpt | grep %d | grep ESTABLISHED | wc -l"%(port)
                print cmd
		connRe = re.compile('\d+$')
	
                status = 0
		try:
			p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
			output = p.stdout.read()

		        for line in output:
		        	if(connRe.match(line) != None):
		        		res = int(line)
		except Exception,e:
			res = sdnlb_conf.max_conns
			self.logger.error("Event server: error while executing netstat command:%s", e)
	
	
		return str(res)
	
	def getCpuLoad(self):
		return str(psutil.cpu_percent())

	def runIperf(self,port):
                timeout = 3 * int(sdnlb_conf.iperf_tout)
                cmd = "timeout"
                args = "%d"%timeout
		cmd2 = "iperf3"
		args2 = "-s" 
		opts = "-p %d"%(port)
                status = 0
                subprocess.call([cmd, args,cmd2,args2,opts])
		return status

	def handle (self,connection, address,port):
		logging.basicConfig(level=logging.DEBUG)
		logger = logging.getLogger("process-%r" % (address,))
		answer = ""
	
		try:
			logger.debug("Event server: client connected %r at %r", connection, address)
	    		msg = connection.recv(2048)
			logger.debug("Event server: received:%s", msg)
			
	    		(msgtype, data) = JsonMessage.parse_json(msg)

			if(msgtype == msgTypes['cmd_req']):
					if data['cmd'] == "iperf":
						port = port+1
						answer = JsonMessage.genCmdAnsMessage("iperf",str(port))
			    			connection.sendall(answer)
						logger.debug("Event server: sent:%s", answer)
						self.runIperf(port)

					elif data['cmd'] == "netstat":
						(ip,port) = address
                                                port = int(data['args'][0])
                                                connections = self.getConnections(port)
						logger.debug("CONNECTIONS:%s"%connections)
						answer = JsonMessage.genCmdAnsMessage("netstat",str(connections))
			    			connection.sendall(answer)
						logger.debug("Event server: sent:%s", answer)

                        # kill iperf process- This must be done with a new command req : for kill iperf
		except:
			logger.exception("Problem handling request")
		finally:
			logger.debug("Closing socket")
                        connection.shutdown(socket.SHUT_RDWR)
			connection.close()

	
		 
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	ip = sys.argv[1]
	port = int(sys.argv[2])
	server = Server(ip, port)

	try:
		server.start()
	except Exception,e:
		logging.exception("Unexpected exception")
		logging.exception(e)
	finally:
		logging.info("Shutting down server")
		for process in multiprocessing.active_children():
			logging.info("Terminating process %r", process)
			process.terminate()
			process.join()
