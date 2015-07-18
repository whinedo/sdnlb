from multiprocessing import Process


class EventListener():

	def __init__(self, port):
		self.port = port
		

	def start(self, queue):
		# start event listener
		p1 = Process(target=self.event_listener)
		p1.start()

	def handleMessage(self,json_msg):
		JsonMessage.parse_json(json_msg)	

	def event_listener(self, queue):
		HOST = ''        # Symbolic name meaning all available interfaces
		json_msg = ''
		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((HOST, self.port))
		s.listen(1)
		
		while 1:
			json_msg = ''
			conn, addr = s.accept()
			print 'Received connection from', addr
			while 1:
				data = conn.recv(1024)
				if not data: 
					break
				json_msg = json_msg + data
			
			conn.close()

			self.handleMessage(json_msg)

