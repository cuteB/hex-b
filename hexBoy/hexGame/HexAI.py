import random

from hexGame.HexBoard import Board

'''
-----------------------------------------------
Main
-----------------------------------------------
'''

class HexAI:
  name = None
  moveAlgorithm = None

  def __init__(self, difficulty = 0):
    self.name = "hexboy"
    print("Am hexboy")

    if (difficulty == 0):
      self.moveAlgorithm = self.randomMove
    else:
      self.moveAlgorithm = self.randomMove

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
