import random

from hexBoy.hex.HexBoard import Board
from hexBoy.hex.HexNode import HexNode
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.AI.agentUtil.BoardEval import BoardStates
from hexBoy.AI.agentUtil.MoveEval import evaluateMove

'''----------------------------------
Random Agent
-----------------------------------'''
class AgentRand(HexAgent):
  # Agent RandRandom moves. Rarely the best
  def __init__(self):
    HexAgent.__init__(self)
    self.name = "Agent_Rand"

  def getAgentMove(self):
    return self._randomMove()
