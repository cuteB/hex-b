from hexGame.HexNode import HexNode
from hexGame.SortedDict import SortedDict
'''
-----------------------------------------------
The PathFinder
-----------------------------------------------
'''
class Pathfinder:
  sortFunc      = None
  getAdjacentSpaces  = None
  getSortValue  = None


  def __init__(self, getAdjacentSpaces, algorithmId = 0):
    self.getAdjacentSpaces = getAdjacentSpaces

    # A*
    if (algorithmId == 0):
      self.sortFunc = self.AStar

    # default is A*
    else:
      self.sortFunc = self.AStar


    def getSortValue(item):
      return item[1].f

    self.getSortValue = getSortValue

  # Get the path
  def findPath(self, nodeDict, startNode, endNode, checkIfBarrier):
    return self.sortFunc(nodeDict, startNode, endNode, checkIfBarrier)

  '''
  ------------------
  AStar
  ------------------
  '''
  def AStar(self, nodes, startPos, endPos, checkIfBarrier):
    # Init open and close SortedDictionaries

    openNodes = SortedDict(getSortValue = self.getSortValue)
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
            # Already in open, Check if this path is better
            if (nextNode.g < (currentNode.g + nextNode.pathCost)):
              nextNode.scoreNode(currentPos, currentNode.g, endPos)
              nodes[nextPos] = nextNode
              openNodes[nextPos] = nextNode

          else:
            # Not in open, Score and add to open
            nextNode.scoreNode(currentPos, currentNode.g, endPos)
            nodes[nextPos] = nextNode
            openNodes[nextPos] = nextNode

    # after loop
    pathPos = nodes[endPos].parent
    path=[]
    while pathPos != None:
      path.append(pathPos)
      pathPos = nodes[pathPos].parent

    return path
