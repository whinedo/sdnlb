from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.examples.load_balancer import *

class LBPolicy(ResonancePolicy):
  def __init__(self, fsm):
    self.fsm = fsm

  def portA_policy(self):                       
    public_ip = IP('10.0.0.100')
    client_ips = [IP('10.0.0.1')]
    repeating_R =  [IP('10.0.0.2')]
    # This will replace the incoming packet[src=10.0.0.1, dst=10.0.0.100] to packet[src=10.0.0.1, dst=10.0.0.2] and
    #                            and packet[src=10.0.0.1, dst=10.0.0.2] back to packet[src=10.0.0.1, dst=10.0.0.100]
    return rewrite(zip(client_ips, repeating_R), public_ip)
    
  def portB_policy(self):
    public_ip = IP('10.0.0.100')
    client_ips = [IP('10.0.0.1')]
    repeating_R =  [IP('10.0.0.3')]
    # This will replace the incoming packet[src=10.0.0.1, dst=10.0.0.100] to packet[src=10.0.0.1, dst=10.0.0.3] and
    #                            and packet[src=10.0.0.1, dst=10.0.0.3] back to packet[src=10.0.0.1, dst=10.0.0.100]
    return rewrite(zip(client_ips, repeating_R), public_ip)

