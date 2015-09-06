#!/usr/bin/env python
import multiprocessing
import time
import socket
from json_message import JsonMessage
import logging
import sys,re
import commands
import psutil

 
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


	def getConnections(self,port,data):
		cmd = "netstat -anp | grep %s | grep ESTABLISHED | wc -l"%port
		connRe = re.compile('\d+$')
	
		status,output = commands.getstatusoutput(cmd)
		res = 0
	
		for line in output:
			if(connRe.match(line) != None):
				res = int(line)/2
	
		return str(res)
	
	def getCpuLoad(self):
		return str(psutil.cpu_percent())
	
	def handle (self,connection, address,port):
		logging.basicConfig(level=logging.DEBUG)
		logger = logging.getLogger("process-%r" % (address,))
		answer = ""
	
		try:
			logger.debug("Connected %r at %r", connection, address)
	
			while True:
				data = connection.recv(1024)
	
				if data == "":
					logger.debug("Socket closed remotely")
					break
	
	
			
				data = data.replace("\r","")
				data = data.replace("\n","")

				logger.debug("Received data %r", data)
	
				if data == "connections":
					answer = self.getConnections(port,data)
				elif data == "cpu":
					answer = self.getCpuLoad()
				else:
					answer = "\n"
	
				connection.sendall(answer)
		except:
			logger.exception("Problem handling request")
		finally:
			logger.debug("Closing socket")
			connection.close()

	
		 
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	port = int(sys.argv[1])
	server = Server("localhost", port)

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