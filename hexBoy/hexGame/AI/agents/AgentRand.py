import random

from hexGame.HexBoard import Board
from hexGame.AI.HexAgent import HexAgent
from hexGame.HexNode import HexNode
from hexGame.AI.agentUtil.BoardEval import BoardStates
from hexGame.AI.agentUtil.MoveEval import evaluateMove

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
