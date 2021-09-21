import random

from hexBoy.hex.HexBoard import Board
from hexBoy.hex.HexNode import HexNode

'''
-----------------------------------------------
HexAgent
-----------------------------------------------
'''
class HexAgent:
  name = "HexBoy"
  player                  = None  # 1: blue or 2: red

  # Board
  gameBoard               = None
  getAdjacentSpaces       = None

  # pathfinder: player positions and barrier checks
  startPos                = None  # player start
  endPos                  = None  # player end
  opponentStart           = None
  opponentEnd             = None
  checkIfBarrier          = None  # player barriers
  checkIfOpponentBarrier  = None  # opponent barriers

  def __init__(self):
    pass # nothing for now

  '''
  -----------------------------------------------
  Public (Override these)
  -----------------------------------------------
  '''
  # Get the next move
  def getAgentMove(self):
    return self._randomMove()

  # Score game and get good. Also reset I guess
  def scoreGame(self):
    return

  # Init board and player
  def setGameBoardAndPlayer(self, gameBoard, player):
    self._initGameBoard(gameBoard)
    self._initPlayerBoard(player)

  '''
  -----------------------------------------------
  Private
  -----------------------------------------------
  '''
  '''
  ------------------
  Agent Setup
  ------------------
  '''
  def _initGameBoard(self, gameBoard):
    self.gameBoard = gameBoard
    self.getAdjacentSpaces = gameBoard.getAdjacentSpaces

  def _initPlayerBoard(self, player):
    self.player = player
    gameBoard = self.gameBoard

    # Blue player
    if (self.player == 1):
      self.startPos = gameBoard.blueStartSpace
      self.endPos = gameBoard.blueEndSpace
      self.opponentStart = gameBoard.redStartSpace
      self.opponentEnd = gameBoard.redEndSpace
      self.checkIfBarrier = HexNode.checkIfBlueBarrierForAI
      self.checkIfOpponentBarrier = HexNode.checkIfRedBarrierForAI

    # Red player
    else:
      self.startPos = gameBoard.redStartSpace
      self.endPos = gameBoard.redEndSpace
      self.opponentStart = gameBoard.blueStartSpace
      self.opponentEnd = gameBoard.blueEndSpace
      self.checkIfBarrier = HexNode.checkIfRedBarrierForAI
      self.checkIfOpponentBarrier = HexNode.checkIfBlueBarrierForAI

  '''
  ------------------
  Random Move
  ------------------
  '''
  def _randomMove(self):
    gameBoard = self.gameBoard
    x = random.randint(0, gameBoard.boardSize - 1)
    y = random.randint(0, gameBoard.boardSize - 1)
    cell = (x,y)

    while (not gameBoard.validateMove((x,y))):
      x = random.randint(0, gameBoard.boardSize - 1)
      y = random.randint(0, gameBoard.boardSize - 1)
      cell = (x,y)

    return cell
