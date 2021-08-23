'''
-----------------------------------------------
Hex Node
-----------------------------------------------
'''
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

  # List of barriers for each player (can't pass a barrier)
    blueSpaces  = [1, 3, 5, 7]
    redSpaces = [2, 4, 6, 8]

  nodeValue = None  # colour (Space) of the hex
  pathCost = None   # Used for path finder algorithm
  parentPos = None # Refrence to parent (tuple)

  # Gonna use these for the heuristic later
  g = None  # Current Score
  h = None  # Heuristic of this node
  f = None  # Combined g + h

  def __init__(self, space):
    self.nodeValue = space
    self.parent = None
    self.pathCost = 1
    self.g = 0
    self.h = 0
    self.f = 0

    if (space == self.Space.BLUE_EDGE or space == self.Space.RED_EDGE):
      self.pathCost = 0

  def getValue(self):
    return self.nodeValue

  def setValue(self, value):
    self.nodeValue = value

  def setParent(self, parent):
    self.parent = parent

  # Score this node and set its parent
  def scoreNode(self, parentPos, parentValue, endPos):
    self.setParent(parentPos)

    # score cost of this node
    self.g = parentValue + self.pathCost

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

  def checkIfEnd(self):
    space = self.getValue()
    print(space)
    return (space == self.Space.RED_END or space == self.Space.BLUE_END)

  def checkIfBlue(self):
    return self.getValue() in HexNode.Space.blueSpaces
