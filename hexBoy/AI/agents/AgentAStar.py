import random

from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.HexBoard import Board
from hexBoy.hex.HexNode import HexNode
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.AI.agentUtil.BoardEval import BoardStates
from hexBoy.AI.agentUtil.MoveEval import evaluateMove

'''----------------------------------
AStar Search Agent
-----------------------------------'''
class AgentAStar(HexAgent):

  def __init__(self):
    HexAgent.__init__(self)
    self.name = "Agent_A*"

  def getAgentMove(self):
    gameBoard = self.gameBoard

    # Find best path to win
    potentialMoves = self.pathfinder.findPath(
      self.startPos,
      self.endPos,
    )

    # make a move on the best path
    random.shuffle(potentialMoves)
    for move in potentialMoves:
      if (gameBoard.validateMove(move)):
        return move

    return self._randomMove()

  def setGameBoardAndPlayer(self, gameBoard, player):
    HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

    def sortFunc(item):
      return item[1].pathCost

    # AStar Pathfinder
    self.pathfinder = PathBoy(
      self.gameBoard,
      self.getAdjacentSpaces,
      self.checkIfBarrier,
      HexNode.getCellValueForNextMove,
      sortFunc
    )
