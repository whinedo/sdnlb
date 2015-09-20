import json

#eventTypes = {'lb': 0}
eventTypes = {'status': 0,
	      'load' : 1}

class JsonMessage (object):

	@staticmethod
	def genStatusMessage(status):
		eventnum = eventTypes['status']

		data = dict(event=dict(event_type=eventnum,    \
		                       description=1,   \
		                       data=dict(data_type='int',     \
		                                 value=status          \
		                       )))


		return json.dumps(data)
		 
	@staticmethod
	def genLoadMessage(cpuLoad,connections):
		eventnum = eventTypes['load']

		data = dict(event=dict(event_type=eventnum,    \
		                       description=1,   \
		                       data=dict(data_type='int',     \
	                      	               value=dict(cpu=cpuLoad,
			      	  		     conns=connections
			      	  		     ))         \
		              	         ))

		return json.dumps(data)

	@staticmethod
	def parse_json(msg):
		json_msg = json.loads(msg)
		
		event_msg = json_msg['event']
		msgtype = event_msg['event_type']
		data = event_msg['data']

		#DEBUG
		print "DATA in JSON:"
		print "JSON:"
		print json_msg
		print "DATA:"
		print data
		#FINDEBUG
		return (msgtype, data)

