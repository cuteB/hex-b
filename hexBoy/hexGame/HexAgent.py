import random

from hexGame.Pathfinder import Pathfinder
from hexGame.HexBoard import Board
from hexGame.HexNode import HexNode

'''
-----------------------------------------------
Main
-----------------------------------------------
'''
class HexAgent:
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

  scoreWin = None
  scoreLoss = None

  def __init__(self,
    player,
    gameBoard,
    difficulty = 0,
    pathfinderId = 1
  ):
    self.name = "HexBoy"
    self.player = player
    self.getAdjacentSpaces = gameBoard.getAdjacentSpaces
    self.pathfinder = Pathfinder(
      self.getAdjacentSpaces,
      pathfinderId
    )

    self.initAgentAlgorithm(difficulty)
    self.initGameBoardForAgent(gameBoard)

  '''
  -----------------------------------------------
  Setup agent
  -----------------------------------------------
  '''
  def initAgentAlgorithm(self, algorithmId):
    # Set algorithm
    if (algorithmId == 0):
      self.name += "(rand)"
      self.moveAlgorithm = self.randomMove

    elif (algorithmId == 1):
      self.name += "(A*)"
      self.moveAlgorithm = self.aStarMove

    elif (algorithmId == 2):
      self.name += "(eval)"
      self.pathfinder = Pathfinder(self.getAdjacentSpaces, 1)
      self.moveAlgorithm = self.strongMove

    else:
      self.name += "(rand)"
      self.moveAlgorithm = self.randomMove


  def initGameBoardForAgent(self, gameBoard):
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
  -----------------------------------------------
  Actions
  -----------------------------------------------
  '''
  def makeMove(self, gameBoard):
    return self.moveAlgorithm(gameBoard)


  '''
  -----------------------------------------------
  Algorithms
  -----------------------------------------------
  '''
  '''
  ------------------
  Random
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
  AStar
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

  '''
  ------------------
  Strong Moves
  ------------------
  '''
  # Find the shortest path to win. Do one of those moves
  def strongMove(self, gameBoard):
    moveNumber = len(gameBoard.moveHistory)

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

    move = self.randomMove(gameBoard)
    moveVal = self.evaluateMove(move, gameBoard, winPath, opponentPath)

    for x in range(gameBoard.boardSize):
      for y in range(gameBoard.boardSize):
        nextMove = (x,y)
        if (gameBoard.validateMove(nextMove)):
          nextVal = self.evaluateMove(nextMove, gameBoard, winPath, opponentPath)
          if (nextVal > moveVal):
            moveVal = nextVal
            move = nextMove

    return move

  def evaluateMove(self, move, gameBoard, winPath, opponentPath):

    value = 1
    if (self.isStrongMove(move, gameBoard)):
      value += 5

    if (move in winPath):
      value += 5

    if (move in opponentPath):
      value += 4

    value += (8 - gameBoard.getDistanceToCenter(move))

    return value

  def isStrongMove(self, move, gameBoard):
    playerMoves = gameBoard.getPlayerMoves()
    (x,y) = move
    strongMoves = [
      (x-2, y+1),
      (x-1, y-1),
      (x-1, y+2),
      (x+1, y+1),
      (x+1, y-2),
      (x+2, y-1)
    ]
    strongDict = {}
    strongDict[strongMoves[0]] = [(x-1,y  ), (x-1,y+1)]
    strongDict[strongMoves[1]] = [(x-1,y  ), (x,  y-1)]
    strongDict[strongMoves[4]] = [(x-1,y+1), (x,  y+1)]
    strongDict[strongMoves[3]] = [(x,  y+1), (x+1,y  )]
    strongDict[strongMoves[2]] = [(x+1,y-1), (x,  y-1)]
    strongDict[strongMoves[5]] = [(x+1,y  ), (x+1,y-1)]

    potentialStrongMoves = []
    for sMove in strongMoves:
      if (gameBoard.isSpaceWithinBounds(sMove)):
        potentialStrongMoves.append(sMove)

    for strongMove in potentialStrongMoves:
      if (strongMove in playerMoves):

        movesToStrongMove = strongDict[strongMove]
        if (not movesToStrongMove[0] in gameBoard.moveHistory
          and not movesToStrongMove[1] in gameBoard.moveHistory
        ):
          return True

    return False

  def spacesNearWinPath(self, winPath, gameBoard):
    nearPath = {}

    for space in winPath:
      adjacentSpaces = self.getAdjacentSpaces(space)
      for closeBy in adjacentSpaces:
        nearPath[closeBy] = closeBy

    return nearPath

  '''
  -----------------------------------------------
  Handle Rewards
  -----------------------------------------------
  '''
  def scoreGame(self, win, gameBoard):
    if (win):
      self.scoreWin(gameBoard)
    else:
      self.scoreLoss(gameBoard)

  def scoreWin(self, gameBoard):
    a = 1

  def scoreLoss(self, gameBoard):
    a = 2
