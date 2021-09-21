'''
-----------------------------------------------
Hex Node
-----------------------------------------------
'''

"""
Probs gotta refactor this Kinda sloppy with how everyone uses it
- values are hard to remember what they are
- Way to manage parents and children
- Count Free spaces properly
"""


class HexNode:
  class Space:
    EMPTY       = 0
    BLUE        = 1
    RED         = 2
    BLUE_EDGE   = 3
    RED_EDGE    = 4
    RED_START   = 5
    BLUE_START  = 6
    RED_END     = 7
    BLUE_END    = 8

  # List of spaces for each player (others are barriers)
    blueSpaces  = [1, 3, 5, 7]
    redSpaces   = [2, 4, 6, 8]

  nodeValue = None  # colour (Space) of the hex
  pathCost  = None  # Used for path finder algorithm. Cost to use this cell
  parentPos = None  # Refrence to parent (tuple)
  nodePos = None    # Node's position
  bestPathCost = None # Used to store the best
  extraPathsToThisNode = None

  # Gonna use these for the heuristic later
  g = None  # Current Score
  h = None  # Heuristic of this node
  f = None  # Combined g + h

  def __init__(self, space, pos):
    self.nodeValue = space
    self.nodePos = pos
    self.parent = None
    self.pathCost = 1
    self.g = 0
    self.h = 0
    self.f = 0

    self.extraPathsToThisNode = 0

    # set the edges to no cost.
    if (space == self.Space.BLUE_EDGE or space == self.Space.RED_EDGE):
      self.pathCost = 0

  def getValue(self):
    return self.nodeValue

  def setValue(self, value):
    self.nodeValue = value

  def setParent(self, parent):
    self.parent = parent

  def setBestPathCost(self, cost):
    self.bestPathCost = cost

  # Score this node and set its parent
  def scoreNode(self, nodeCost, parentPos, parentValue, endPos):
    self.setParent(parentPos)

    # score cost of this node (previous cost + node cost)
    self.g = parentValue + nodeCost

    # score heuristic
    if (self.checkIfBlue()):
      # score blue based on difference in y values
      self.h = abs(endPos[1] - parentPos[1])
    else:
      # score red based on difference in x values
      self.h = abs(endPos[0] - parentPos[0])

    # Add them up for f
    self.f = self.g + self.h

  def checkIfRedBarrier(node):
    space = node.getValue()
    return (space in HexNode.Space.blueSpaces or space == HexNode.Space.EMPTY)

  def checkIfBlueBarrier(node):
    space = node.getValue()
    return (space in HexNode.Space.redSpaces or space == HexNode.Space.EMPTY)

  def checkIfRedBarrierForAI(node):
    space = node.getValue()
    return (space in HexNode.Space.blueSpaces)

  def checkIfBlueBarrierForAI(node):
    space = node.getValue()
    return (space in HexNode.Space.redSpaces)

  def checkIfEnd(self):
    space = self.getValue()
    return (space == self.Space.RED_END or space == self.Space.BLUE_END)

  def checkIfBlue(self):
    return self.getValue() in HexNode.Space.blueSpaces

  def getCellValueForWinningPath(hexnode):
    spaces = HexNode.Space
    if (hexnode.nodeValue == spaces.BLUE_EDGE or hexnode.nodeValue == spaces.RED_EDGE):
      return 0
    else:
      return 1

  def getCellValueForNextMove(hexnode):
    spaces = HexNode.Space
    if (hexnode.nodeValue == spaces.BLUE_EDGE or hexnode.nodeValue == spaces.RED_EDGE):
      return 0

    elif (hexnode.nodeValue == spaces.EMPTY):
      return 1

    elif (hexnode.nodeValue == spaces.BLUE or hexnode.nodeValue == spaces.RED):
      return 0

    else:
      return 1

  def addExtraPathsToNode(self, paths):
    self.extraPathsToThisNode += paths

  def setExtraPathsToNode(self, paths):
    self.extraPathsToThisNode = paths
