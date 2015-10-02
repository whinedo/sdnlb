from multiprocessing import Process
import time
import commands
from socketconnection import SocketConnection
from json_message import *
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

	def eventBeat(self):
		for service in self.services.getServices():
			index = 0
                        processes = []
			for server in service.getServers():
         			eventPort = server.getEventPort()
                                p = Process(target=self.eventBeatWorker, args=(service.getLbPort(),eventPort,self.services,index))
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

        def eventBeatWorker(self,lbPort,eventPort,services,index):
            server = services.getServer(lbPort,index)
	    socket = SocketConnection()
	    try:
	    	socket.connect(server.getIp(),int(eventPort),30)
		cmd = "iperf"
		msg = JsonMessage.genCmdReqMessage(cmd)
		socket.send(msg)
	    	msg = socket.receive()
	    	
	    	if msg != '':
	    		(msgtype, data) = JsonMessage.parse_json(msg)
			
			if (msgtype == msgTypes['cmd_ans']):
				if (data['cmd'] == "iperf"):
					port = int(data['args'])
					time.sleep(2) # wait for iperf to start running	
                                        cmd = "iperf"
                                        args = "-c"
					opts = "%s -t %d -p %d -J"%(ip,int(sdnlb_conf.iperf_tout),int(port))
                		        status = 0
                		        output = subprocess.check_output([cmd, args,opts])
				
		                	json_msg = JsonMessage.parse_iperf_json
                 #       if 'value' in data.keys():
                 #               value = data['value']

	    	 #       	if 'cpu' in value.keys():
	    	 #       		server.setCpu(float(value['cpu']))

	    	 #       	if 'conns' in value.keys():
	    	 #       		server.setConnections(int(value['conns']))


            except Exception,e:
	    	# cannot connect with server
                #print "Exception"
	    	#print e
	    	#print "STATUS DOWN"
                server.setStatus(False)
	    finally:
	    	socket.close()

	    services.setServer(lbPort,server,index=index)

