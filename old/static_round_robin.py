from pyretic.lib.corelib import *
from pyretic.lib.std import *



def mac_learner():
    """Create a dynamic policy object from learn()"""
    return dynamic(learn)()

def main():
    return mac_learner()

