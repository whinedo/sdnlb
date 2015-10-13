from ilbagorithm import LBAlgorithm
from round_robin import RoundRobin
from weight_round_robin import WeightRoundRobin
from least_load import LeastLoad

class AlgoFactory(object):

        @staticmethod
        def getAlgoInstance(type):
            algo = None

            if type == "round":
                algo = RoundRobin()
            elif type == "weight":
                algo = WeightRoundRobin()
            elif type == "connections":
                algo = LeastConnections()
            elif type == "cpu":
                algo = LeastLoad()
    
            if algo == None:
                algo = RoundRobin()
    
            return algo
