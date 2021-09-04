import random

from hexGame.Pathfinder import Pathfinder
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
class RLAgent(HexAgent):

  def __init__(self):
    HexAgent.__init__(self)
