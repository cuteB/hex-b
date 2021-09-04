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
class AgentStrong(HexAgent):

  def __init__(self):
    HexAgent.__init__(self)
    self.name = "Agent_Strong"

    # Pathfinder
    self.pathfinder = Pathfinder(
      self.getAdjacentSpaces,
      1 #AStar
    )
  '''
  -----------------------------------------------
  Agent Functions
  -----------------------------------------------
  '''
  # Override
  def getAgentMove(self):
    gameBoard = self.gameBoard

    winPath = self.pathfinder.findPath(
      gameBoard.getNodeDict(),
      self.startPos,
      self.endPos,
      self.checkIfBarrier,
      HexNode.getCellValueForNextMove
    )
    opponentPath = self.pathfinder.findPath(
      gameBoard.getNodeDict(),
      self.opponentStart,
      self.opponentEnd,
      self.checkIfOpponentBarrier,
      HexNode.getCellValueForNextMove
    )

    move = self._randomMove()
    moveVal = evaluateMove(move, gameBoard, winPath, opponentPath)

    for x in range(gameBoard.boardSize):
      for y in range(gameBoard.boardSize):
        nextMove = (x,y)
        if (gameBoard.validateMove(nextMove)):
          nextVal = evaluateMove(nextMove, gameBoard, winPath, opponentPath)
          if (nextVal > moveVal):
            moveVal = nextVal
            move = nextMove

    return move

  # Override
  def setGameBoardAndPlayer(self, gameBoard, player):
    HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

    # AStar Pathfinder
    self.pathfinder = Pathfinder(
      self.getAdjacentSpaces,
      1 #AStar
    )
