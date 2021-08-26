from hexGame.HexNode import HexNode
from hexGame.SortedDict import SortedDict
'''
-----------------------------------------------
The PathFinder
-----------------------------------------------
'''
class Pathfinder:
  pathFunc            = None  # The type of pathfinding algorithm to use
  getAdjacentSpaces   = None  # funciton, get adjacent spaces of cell
  getSortValue        = None  # function to get the value to use for sorting


  def __init__(self, getAdjacentSpaces, algorithmId = 0):
    self.getAdjacentSpaces = getAdjacentSpaces

    # A*
    if (algorithmId == 0):
      self.pathFunc = self.AStar

    # default is A*
    else:
      self.pathFunc = self.AStar


    def getSortValue(item):
      return item[1].f

    self.getSortValue = getSortValue

  # Get the path using the defined pathfinding algorithm
  def findPath(self, nodeDict, startNode, endNode, checkIfBarrier, getCellCost):
    return self.pathFunc(nodeDict, startNode, endNode, checkIfBarrier, getCellCost)

  '''
  ------------------
  AStar
  ------------------
  '''
  def AStar(self, nodes, startPos, endPos, checkIfBarrier, getCellCost):
    # Init open and close SortedDictionaries
    # Open: add newly found nodes to this and pop off to get the next node to
    # look at
    openNodes = SortedDict(getSortValue = self.getSortValue)
    # Closed: contains all nodes that have been looked at already
    closedNodes = SortedDict()

    # Get hex space ids
    spaces = HexNode.Space

    currentPos = startPos
    currentNode = nodes[currentPos]
    openNodes[currentPos] = currentNode

    adjacentSpaces = None
    nextNode = None

    # loop while the end hasn't been found
    while (currentPos != endPos):
      # All nodes have been looked at, return no path
      if (len(openNodes) == 0):
        return []

      # keep looking for path
      # pop off the next node in open and close it
      currentPos, currentNode = openNodes.popItem()
      closedNodes[currentPos] = None

      adjacentSpaces = self.getAdjacentSpaces(currentPos)
      for nextPos in adjacentSpaces:
        nextNode = nodes[nextPos]

        # Only check if not a barrier and not in closed
        if (not checkIfBarrier(nextNode) and not closedNodes.hasKey(nextPos)):
          if openNodes.hasKey(nextPos):
            # Already in open,
            # Check if the current value of the node is more than the
            # cost from the current node would be.
            if (nextNode.g > (currentNode.g + getCellCost(nextNode))):
              nextNode.scoreNode(getCellCost(nextNode), currentPos, currentNode.g, endPos)
              nodes[nextPos] = nextNode
              openNodes[nextPos] = nextNode

          else:
            # Not in open, Score and add to open
            nextNode.scoreNode(getCellCost(nextNode), currentPos, currentNode.g, endPos)
            nodes[nextPos] = nextNode
            openNodes[nextPos] = nextNode

    # after loop
    pathPos = nodes[endPos].parent
    path=[]
    while pathPos != None:
      path.append(pathPos)
      pathPos = nodes[pathPos].parent

    return path
