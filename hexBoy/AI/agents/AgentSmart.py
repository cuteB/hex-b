from hexBoy.hex.HexBoard import Board
from hexBoy.AI.HexAgent import HexAgent

'''
-----------------------------------------------
Reinforcement Learning Agent
-----------------------------------------------
'''
class AgentSmart(HexAgent):
    # AgentSmart thinks two moves ahead
    def __init__(self):
        HexAgent.__init__(self)
        self.name = "Agent_Smart"

    '''
    -----------------------------------------------
    Agent Functions (Overrides)
    -----------------------------------------------
    '''
    def getAgentMove(self):
        # get best path.

        # check connections along best path

        #


        # default random move
        return self._randomMove()

