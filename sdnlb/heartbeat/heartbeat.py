from multiprocessing import Process
import time
import commands
from socketconnection import SocketConnection
from json_message import *
from subprocess import Popen, PIPE, STDOUT
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
		#DEBUG
                print "eventBeat"
		#FINDEBUG

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
	    	#socket.connect(server.getIp(),int(eventPort),30)
	    	socket.connect(server.getIp(),int(eventPort),int(sdnlb_conf.iperf_tout)*3)
		cmd = "iperf"
		msg = JsonMessage.genCmdReqMessage(cmd)
		socket.send(msg)
	    	msg = socket.receive()
	    	
	    	if msg != '':
	    		(msgtype, data) = JsonMessage.parse_json(msg)
			
			if (msgtype == msgTypes['cmd_ans']):
				if (data['cmd'] == "iperf"):
					port = int(data['args'])
					time.sleep(4) # wait for iperf to start running	
					cmd = 'iperf3 -c %s -t %d -p %d -J'%(server.getIp(),int(sdnlb_conf.iperf_tout),int(port))

	                                p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
	                                output = p.stdout.read()
			                json_msg = JsonMessage.parse_iperf_json(output)
					if (json_msg['end']['cpu_utilization_percent']['remote_system'] != None):
						#cpu_load = json_msg['end']['cpu_utilization_percent']['remote_system']
						cpu_load = json_msg['end']['cpu_utilization_percent']['remote_total']
						#DEBUG
                                                print "CPU_LOAD:",cpu_load
						#FINDEBUG
						server.setCpu(float(cpu_load))

            except Exception,e:
	    	# cannot connect with server
                #print "Exception"
	    	#print e
	    	#print "STATUS DOWN"
                server.setStatus(False)
	    finally:
	    	socket.close()
            print "%d,%d"%(server.getCpu(),index)
	    services.setServer(lbPort,server,index=index)

