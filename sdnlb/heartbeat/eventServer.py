#!/usr/bin/env python
import multiprocessing
import time
import socket
from json_message import *
import logging
import sys,re
import subprocess
import psutil
import sdnlb_conf

 
class Server (object):

	def __init__(self, hostname, port):
		self.logger = logging.getLogger("server")
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
                cmd = "netstat"
		args = "-anp | grep %s | grep ESTABLISHED | wc -l"%port
		connRe = re.compile('\d+$')
	
                status = 0
                output = subprocess.check_output([cmd, args])
		res = 0
	
		for line in output:
			if(connRe.match(line) != None):
				res = int(line)/2
	
		return str(res)
	
	def getCpuLoad(self):
		return str(psutil.cpu_percent())

	def runIperf(self,port):
                cmd = "iperf"
		args = " -s -p %d "%(port+1)
                status = 0
                output = subprocess.check_output([cmd, args])
		return status
	
	def handle (self,connection, address,port):
		logging.basicConfig(level=logging.DEBUG)
		logger = logging.getLogger("process-%r" % (address,))
		answer = ""
	
		try:
			logger.debug("Connected %r at %r", connection, address)
	    		msg = connection.recv(2048)
                        #DEBUG
                        print "MSG:",msg
                        #FINDEBUG
			
	    		(msgtype, data) = JsonMessage.parse_json(msg)

			if(msgtype == msgTypes['cmd_req']):
					if data['cmd'] == "iperf":
						port = port+1
						answer = JsonMessage.genCmdAnsMessage("iperf",str(port))
						self.runIperf(port)

	                if (len(answer)>0):
			    connection.sendall(answer)
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
