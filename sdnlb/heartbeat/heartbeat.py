from multiprocessing import Process
import time
from socketconnection import SocketConnection
from json_message import JsonMessage
import sdnlb_conf

class HeartBeat (object):

	def __init__(self,ip,services,sendEvent=False):
		self.services = services
		self.sendEvent = sendEvent
		self.timeout = sdnlb_conf.hb_timeout
		self.ip = ip

	def getIp(self):
		return self.ip

	def start(self):
		# start event listener
		p1 = Process(target=self.main)
		p1.start()

	def main(self):
		while True:
			self.heartBeat()
			
			if (self.sendEvent):
				self.eventBeat()

			time.sleep(self.timeout)

	def heartBeat(self):
		for service in self.services.getServices():
			index = 0
			lbPort = service.getLbPort()
			for server in service.getServers():

				socket = SocketConnection()

				try:
					socket.connect(server.getIp(),server.getPort())
					print "STATUS OK"
					server.setStatus(True)
				except Exception,e:
					# cannot connect with server
					#print e
					#print "STATUS DOWN"
					server.setStatus(False)
				finally:
					socket.close()

				self.services.setServer(lbPort,server,index=index)
				index += 1

		#DEBUG
		for service in self.services.getServices():
			for server in service.getServers():
				print "STATUS:",server.getStatus()
		#FINDEBUG

        def eventBeatWorker(self,lbPort,server,index):
	    socket = SocketConnection()
	    try:
	    	socket.connect(server.getIp(),server.getEventPort())
	    	msg = socket.recv()
	    	
	    	if msg != '':
	    		(msgtype, data) = JsonMessage.parse_json(msg)

                        print "data:",data

	    		if cpu in data:
	    			server.setCpu(data['cpu'])

	    		if conns in data:
	    			server.setCpu(data['conns'])

                        print data
            except Exception,e:
	    	# cannot connect with server
	    	#print e
	    	#print "STATUS DOWN"
                server.setStatus(False)
	    finally:
	    	socket.close()

	    self.services.setServer(lbPort,index,server)

	def eventBeat(self):
		for service in self.services.getServices():
			index = 0
                        processes = []
			for server in service.getServers():
         			eventPort = server.getEventPort()
                                p = Process(target=self.eventBeatWorker, args=(service.getLbPort(),server,index))
                                p.start()
                                processes.append(p)
			        index += 1

                        for p in processes:
                                p.join()

		#DEBUG
		for service in self.services.getServices():
			for server in service.getServers():
				print "STATUS:",server.getStatus()
				print "CPU:",server.getCpu()
				print "CONNS:",server.getConnections()
		#FINDEBUG
