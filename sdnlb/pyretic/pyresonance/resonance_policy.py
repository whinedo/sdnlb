################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *

class ResonancePolicy():

  state_policy_map = {}

  def __init__(self):
    self.state_policy_map['default'] = self.default_policy

  def get_policy(self, state):
    if self.state_policy_map.has_key(state):
      return self.state_policy_map[state]
    else:
      return self.default_policy
    
  """ Default state policy """
  def default_policy(self):
    return drop


