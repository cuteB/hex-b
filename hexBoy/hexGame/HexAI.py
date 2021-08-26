import random

from hexGame.Pathfinder import Pathfinder
from hexGame.HexBoard import Board
from hexGame.HexNode import HexNode

'''
-----------------------------------------------
Main
-----------------------------------------------
'''

class HexAI:
  name = None
  moveAlgorithm = None
  pathfinder = None

  # AStar stuff
  getAdjacentSpaces = None
  checkIfBarrier = None
  checkIfOpponentBarrier = None

  # player stuff
  player = None
  startPos = None
  endPos = None
  opponentStart = None
  opponentEnd = None

  def __init__(self,
    player,
    gameBoard,
    difficulty = 0,
  ):
    self.name = "hexboy"
    self.player = player
    self.getAdjacentSpaces = gameBoard.getAdjacentSpaces

    if (difficulty == 0):
      self.name += " (rand)"
      self.moveAlgorithm = self.randomMove
    elif (difficulty == 1):
      self.name += " (A*)"
      self.pathfinder = Pathfinder(self.getAdjacentSpaces, 1)
      self.moveAlgorithm = self.aStarMove

    else:
      self.name += " (rand)"
      self.moveAlgorithm = self.randomMove

    # Blue AI
    if (self.player == 1):
      self.startPos = gameBoard.blueStartSpace
      self.endPos = gameBoard.blueEndSpace

      self.opponentStart = gameBoard.redStartSpace
      self.opponentEnd = gameBoard.redEndSpace

      self.checkIfBarrier = HexNode.checkIfBlueBarrierForAI
      self.checkIfOpponentBarrier = HexNode.checkIfRedBarrierForAI

    # Red AI
    else:
      self.startPos = gameBoard.redStartSpace
      self.endPos = gameBoard.redEndSpace

      self.opponentStart = gameBoard.blueStartSpace
      self.opponentEnd = gameBoard.blueEndSpace

      self.checkIfBarrier = HexNode.checkIfRedBarrierForAI
      self.checkIfOpponentBarrier = HexNode.checkIfBlueBarrierForAI

  def makeMove(self, gameBoard):
    return self.moveAlgorithm(gameBoard)

  '''
  ------------------
  Random algorithm
  ------------------
  '''
  def randomMove(self, gameBoard):
    x = random.randint(0, gameBoard.boardSize - 1)
    y = random.randint(0, gameBoard.boardSize - 1)
    cell = (x,y)

    while (not gameBoard.validateMove((x,y))):
      x = random.randint(0, gameBoard.boardSize - 1)
      y = random.randint(0, gameBoard.boardSize - 1)
      cell = (x,y)

    return cell

  '''
  ------------------
  AStar algorithm
  ------------------
  Find the shortest path to win. Do one of those moves
  '''
  def aStarMove(self, gameBoard):
    def getSortValue(cell):
      node = gameBoard.getNodeDict()[cell]
      return HexNode.getCellValueForNextMove(node)

    potentialMoves = self.pathfinder.findPath(
      gameBoard.getNodeDict(),
      self.startPos,
      self.endPos,
      self.checkIfBarrier,
      HexNode.getCellValueForNextMove
    )

    random.shuffle(potentialMoves)
    for move in potentialMoves:
      if (gameBoard.validateMove(move)):
        return move

    return self.randomMove(gameBoard)
