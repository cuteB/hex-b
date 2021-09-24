import copy

from hexBoy.hex.HexNode import HexNode

"""
  Changes
  - Need to modify the board to help out the pathfinder
    - Each agent needs to modify values of the nodes to save time
    - Need to get available moves and future states quick without breaking the
      board for the other player
  - IDEA commit the current board to mem. then make moves to find future states
    - then reset board to last commit or commit the next move

  Needs to be faster for pathfinder
  - Need to look deeper faster

  IDEA: make a board for pathfinders to modify values for their nodes

"""


'''----------------------------------
Hex Board
-----------------------------------'''
# TODO change name to hexboard
class Board:
  boardDict       = None  # dict<HexNode>, Cells on the board and their values
  boardSize       = None  # int, size of the board
  moveHistory        = None # List of moves in order

  # HexNode.Space, object of the different types of hex spaces.
  hexTypes        = None

  # tuples of the (x,y) coordinates of the red/blue start/end spaces
  redStartSpace   = None
  redEndSpace     = None
  blueStartSpace  = None
  blueEndSpace    = None

  def __init__(self, boardSize):
    self.boardSize = boardSize
    self.hexTypes = HexNode.Space
    self.moveHistory = []

    self.redStartSpace = (-1, 5)
    self.redEndSpace = (self.boardSize, 5)
    self.blueStartSpace = (5, -1)
    self.blueEndSpace = (5, self.boardSize)

    self.boardDict = self.initGameBoard()

  # Return the board node dict
  def getNodeDict(self):
    return self.boardDict

  # Initialize the starting game board.
  def initGameBoard(self):
    dict = {}

    #initialize playing spaces
    for x in range(self.boardSize):
      for y in range(self.boardSize):
        dict[(x,y)] = HexNode(self.hexTypes.EMPTY, (x,y))

    # Itialize edges in dict
    # blue edge
    for x in range(self.boardSize):
      dict[(x,-1)] = HexNode(self.hexTypes.BLUE_EDGE, (x,-1))
      dict[(x,self.boardSize)] = HexNode(self.hexTypes.BLUE_EDGE, (x,self.boardSize))
    # red edge
    for y in range(self.boardSize):
      dict[(-1,y)] = HexNode(self.hexTypes.RED_EDGE, (-1,y))
      dict[(self.boardSize,y)] = HexNode(self.hexTypes.RED_EDGE, (self.boardSize,y))

    return dict

  def setBoardDict(self, dict):
    self.boardDict = dict

  # Check if the given cell is a valid move. (hex is empty)
  def validateMove(self, cell):
    return cell != None and self.isSpaceWithinBounds(cell) and self.boardDict[cell].getValue() == self.hexTypes.EMPTY

  # Make the move on the board dict, add to move history
  def makeMove(self, cell, player):
    self.moveHistory.append(cell)
    self.boardDict[cell].setValue(player)

  # Check if the move is within the board or edges
  def isSpaceWithinBounds(self, cell):
    boardSize = self.boardSize
    (x,y) = cell

    # include the edges around the matrix, cells within [-1, boardsize] bound.
    return (x >= -1 and y >= -1
      and x <= boardSize and y <= boardSize
      # Don't include (-1,-1), (-1, len), (len, -1), (len, len)
      and not ((x == -1 or x == boardSize) and (y == -1 or y == boardSize)))

  # Get adjacent spaces
  def getAdjacentSpaces(self, cell):
    '''
    Here is what the hex space looks like. just treat them like squares
    with too extra edges
     ___
    /0,0\___
    \___/1,0\___
    /0,1\___/2,0\___
    \___/1,1\___/3,0\___
    /0,2\___/2,1\___/4,0\
    \___/1,2\___/3,1\___/
    /0,3\___/2,2\___/4,1\
    \___/1,3\___/3,2\___/
    /0,4\___/2,3\___/4,2\
    \___/1,4\___/3,3\___/
        \___/2,4\___/4,3\
            \___/3,4\___/
                \___/4,4\
                    \___/
    '''
    x = cell[0]
    y = cell[1]

    # eg for cell       (1,1)
    adjacentSpaces = []
    potentialSpaces = [
      (x,   y-1),     # (1,0) up
      (x,   y+1),     # (1,2) down
      (x-1, y),       # (0,1) left
      (x+1, y),       # (2,1) right
      (x-1, y+1),     # (0,2) down+left
      (x+1, y-1),     # (2,0) up+right
    ]

    # validate the potential spaces and return the adjacent spaces
    for space in potentialSpaces:
      if (self.isSpaceWithinBounds(space)):
        adjacentSpaces.append(space)

    return adjacentSpaces

  # XXX Don't really like this anymore. Remove it probably
  def get2AwaySpaces(self, cell):
    # return nodes within 2 spaces of the cell
    x = cell[0]
    y = cell[1]

    adjacentSpaces = []
    potentialSpaces = [
      (x-2, y),
      (x-2, y+1),
      (x-2, y+2),
      (x-1, y-1),
      (x-1, y+2),
      (x,   y-2),
      (x,   y+2),
      (x+1, y+1),
      (x+1, y-2),
      (x+2, y),
      (x+2, y-1),
      (x+2, y-2),
    ]

    # validate the potential spaces and return the adjacent spaces
    for space in potentialSpaces:
      if (self.isSpaceWithinBounds(space)):
        adjacentSpaces.append(space)

    return adjacentSpaces

  def resetGame(self):
    self.boardDict = self.initGameBoard()
    self.moveHistory = []

  '''
  ------------------
  Functions for moves
  ------------------
  '''
  # TODO this is wrong for hexes,
  def getDistanceToCenter(self, move):
    (x,y) = move
    center = int(self.boardSize // 2)


    return abs(x-center) + abs(y-center)

  # COMBAK not sure if this is how I want to deal with this
  def getPlayerMoves(self, playerId=None):
    playerMoves = []
    if (playerId != None):
      player = playerId - 1
    else :
      player = (len(self.moveHistory) % 2)

    for i in range(len(self.moveHistory)):
      if (i % 2 == player):
        playerMoves.append(self.moveHistory[i])

    return playerMoves

  '''
  ------------------
  Functions for board
  ------------------
  '''
  # FIXME these two functions are ugly and bad
  # return a copy of the current board
  def getBoardFromMove(self, move, player):
    boardCopy = Board(self.boardSize)
    dictCopy = copy.deepcopy(self.getNodeDict())
    boardCopy.setBoardDict(dictCopy)

    boardCopy.makeMove(move, player)

    return boardCopy

  # return a list of possible moves in this board
  def getPossibleMoves(self):
    possibleMoves = []

    for x in range(self.boardSize):
      for y in range(self.boardSize):
        if (self.validateMove((x,y))):
          possibleMoves.append((x,y))

    return possibleMoves
