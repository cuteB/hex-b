import random

from hexBoy.HexBoard import Board
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.HexNode import HexNode
from hexBoy.AI.agentUtil.BoardEval import BoardStates
from hexBoy.AI.agentUtil.MoveEval import evaluateMove

'''
-----------------------------------------------
Reinforcement Learning Agent
-----------------------------------------------
'''
class AgentRand(HexAgent):
  # Agent RandRandom moves. Rarely the best
  def __init__(self):
    HexAgent.__init__(self)
    self.name = "Agent_Rand"

  '''
  -----------------------------------------------
  Agent Functions (Overides)
  -----------------------------------------------
  '''
  def getAgentMove(self):
    return self._randomMove()
