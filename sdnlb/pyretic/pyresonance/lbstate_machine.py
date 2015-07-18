from resonance_states import ResonanceStateMachine

EVENT_TYPE_LB = 0


class LBStateMachine(ResonanceStateMachine): 

    def handleMessage(self, msg, queue):

        msgtype, host, next_state = self.parse_json(msg)        

        # Add the state transition logic
        # hint: use the state_transition function   
        if msgtype == EVENT_TYPE_LB:    
            self.state_transition(next_state, host, queue)	        

    def get_portA_hosts(self):
        # return <list of host in portA state> # hint: use the get_hosts_in_state function
        return self.get_hosts_in_state('portA')

    def get_portB_hosts(self):
        #return <list of host in portB state> # hint: use the get_hosts_in_state function
        return self.get_hosts_in_state('portB')
