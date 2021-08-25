from hexGame.HexNode import HexNode

'''
-----------------------------------------------
Game Board
-----------------------------------------------
'''
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

    self.redStartSpace = (-1, 0)
    self.redEndSpace = (self.boardSize, self.boardSize - 1)
    self.blueStartSpace = (0, -1)
    self.blueEndSpace = (self.boardSize -1, self.boardSize)

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
        dict[(x,y)] = HexNode(self.hexTypes.EMPTY)

    # Itialize edges in dict
    # blue edge
    for x in range(self.boardSize):
      dict[(x,-1)] = HexNode(self.hexTypes.BLUE_EDGE)
      dict[(x,self.boardSize)] = HexNode(self.hexTypes.BLUE_EDGE)
    # red edge
    for y in range(self.boardSize):
      dict[(-1,y)] = HexNode(self.hexTypes.RED_EDGE)
      dict[(self.boardSize,y)] = HexNode(self.hexTypes.RED_EDGE)

    return dict

  # Check if the given cell is a valid move. (hex is empty)
  def validateMove(self, cell):
    return self.boardDict[cell].getValue() == self.hexTypes.EMPTY

  # Make the move on the board dict, add to move history
  def makeMove(self, cell, player):
    self.moveHistory.append(cell)
    self.boardDict[cell].setValue(player)

  # Check if the move is within the board or edges
  def isSpaceWithinBounds(self, cell):
    boardSize = self.boardSize
    x = cell[0]
    y = cell[1]

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
    \___/1,1\___/3,0\
    /0,2\___/2,1\___/
    \___/1,2\___/3,1\
    /0,3\___/2,2\___/
    \___/1,3\___/3,2\
        \___/2,3\___/
            \___/3,3\
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
