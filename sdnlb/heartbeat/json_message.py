import json

#eventTypes = {'lb': 0}
msgTypes = {'cmd_req': 0,
            'cmd_ans':1,
	      'info' : 2}

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
		                       data=dict(data_type='float',     \
	                      	               value=dict(cpu=cpuLoad,
			      	  		     conns=connections
			      	  		     ))         \
		              	         ))

		return json.dumps(data)

	@staticmethod
	def genCmdReqMessage(command,arguments):
                msgType = msgTypes['cmd_req']

                data = dict(msgtype=msgType,data=dict(cmd=command,args=arguments))

		return json.dumps(data)

	@staticmethod
	def genCmdAnsMessage(command,arguments):
                msgType = msgTypes['cmd_ans']

                data = dict(msgtype=msgType,data=dict(cmd=command,args=arguments))

		return json.dumps(data)

	@staticmethod
	def parse_iperf_json(msg):
		json_msg = json.loads(msg)
		return json_msg
		
	@staticmethod
	def parse_json(msg):
		json_msg = json.loads(msg)
		
		msgtype = json_msg['msgtype']
		data = json_msg['data']

		return (msgtype, data)

