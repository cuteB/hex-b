import random

from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.HexBoard import Board
from hexBoy.hex.HexNode import HexNode
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.AI.agentUtil.BoardEval import BoardStates
from hexBoy.AI.agentUtil.MoveEval import evaluateMove

'''----------------------------------
Strong move Agent
----------------------------------'''
class AgentStrong(HexAgent):

  def __init__(self):
    HexAgent.__init__(self)
    self.name = "Agent_Strong"

  '''---
  Agent Functions
  ---'''
  # Override
  def getAgentMove(self):
    gameBoard = self.gameBoard

    winPath = self.pathfinder.findPath(
      self.startPos,
      self.endPos,
    )


    opponentPath = self.oppPathFinder.findPath(
      self.opponentStart,
      self.opponentEnd,
    )

    move = self._randomMove()
    moveVal = evaluateMove(move, gameBoard, winPath, opponentPath, self.player)

    for x in range(gameBoard.boardSize):
      for y in range(gameBoard.boardSize):
        nextMove = (x,y)
        if (gameBoard.validateMove(nextMove)):
          nextVal = evaluateMove(nextMove, gameBoard, winPath, opponentPath, self.player)
          if (nextVal > moveVal):
            moveVal = nextVal
            move = nextMove

    return move

  # Override
  def setGameBoardAndPlayer(self, gameBoard, player):
    HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

    self.pathfinder = PathBoy(
      self.gameBoard,
      self.getAdjacentSpaces,
      self.checkIfBarrier,
      HexNode.getCellValueForNextMove,
    )

    self.oppPathFinder = PathBoy(
      self.gameBoard,
      self.getAdjacentSpaces,
      self.checkIfOpponentBarrier,
      HexNode.getCellValueForNextMove,
    )
