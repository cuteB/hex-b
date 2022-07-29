import random

from hexBoy.hex.HexBoard import Board
from hexBoy.hex.HexNode import HexNode
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.AI.agentUtil.BoardEval import BoardStates
from hexBoy.AI.agentUtil.MoveEval import evaluateMove

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
    return self._randomMove()



  '''
  -----------------------------------------------
  utility functions
  -----------------------------------------------
  '''




  


