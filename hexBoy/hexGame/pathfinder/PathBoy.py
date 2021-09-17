import copy

from hexGame.HexNode import HexNode
from hexGame.SortedDict import SortedDict


'''
-----------------------------------------------
The PathFinder
-----------------------------------------------
'''
class PathBoy:
  pathFunc            = None  # The type of pathfinding algorithm to use
  getAdjacentSpaces   = None  # funciton, get adjacent spaces of cell
  getSortValue        = None  # function to get the value to use for sorting

  def __init__(self, getAdjacentSpaces, algorithmId = 0, sortFunc = None):
    self.getAdjacentSpaces = getAdjacentSpaces

    # A*
    if (algorithmId == 0):
      self.pathFunc = self.AStar

    # default is A*
    else:
      self.pathFunc = self.AStar

    def getSortValue(item):
      return item[1].f

    if (sortFunc == None):
      self.getSortValue = getSortValue
    else:
      self.getSortValue = sortFunc

  # Get the path using the defined pathfinding algorithm
  def findPath(self, nodeDict, startNode, endNode, checkIfBarrier, getCellCost):
    return self.pathFunc(nodeDict, startNode, endNode, checkIfBarrier, getCellCost)

  def getNumBestPaths(self, nodeDict, startNode, endNode, checkIfBarrier, getCellCost):
    self.NumBestPaths(self, nodeDict, startNode, endNode, checkIfBarrier, getCellCost)

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


  '''
  ------------------
  score path
  ------------------
  '''
  def ScorePath(self, nodes, path, getCellCost):
    cost = 0
    stepNode = None
    for step in path:
      stepNode = nodes[step]
      cost += getCellCost(stepNode)

    return cost

  def getParentPath(self, nodes, endPos):
      pathPos = nodes[endPos].parent
      path=[]
      while pathPos != None:
        path.append(pathPos)
        pathPos = nodes[pathPos].parent

      return path

  '''
  ------------------
  Best paths
  ------------------
  '''
  def NumBestPaths(self, nodes, startPos, endPos, checkIfBarrier, getCellCost):
    spaces = HexNode.Space
    numPaths = SortedDict()

    winPath = self.AStar(nodes, startPos, endPos, checkIfBarrier, getCellCost)
    bestCost = self.ScorePath(nodes, winPath, getCellCost)


    openNodes = SortedDict(getSortValue = self.getSortValue)
    closedNodes = SortedDict()
    endNodes = SortedDict() # nodes to add up to get the number of paths

    # add starting position to pop off
    currentPos = startPos
    currentNode = nodes[currentPos]
    currentNode.setExtraPathsToNode(0.25)
    openNodes[currentPos] = currentNode

    adjacentSpaces = None
    nextNode = None
    closedNode = None

    # helper functions
    def setNodeInOpenNodes(pos):
      nextNode.scoreNode(getCellCost(nextNode), currentPos, currentNode.g, endPos)
      nonlocal numPaths

      # check if this pos is on the winning edge and moving from a non edge
      # to an end edge
      if ((nextNode.nodeValue == spaces.BLUE_EDGE or nextNode.nodeValue == spaces.RED_EDGE)
        and (currentNode.nodeValue != spaces.BLUE_EDGE or currentNode.nodeValue != spaces.RED_EDGE)
        and nextNode.g == bestCost
      ):
        # node is an edge and has the best cost -> is a winning path
        # add paths to the total paths
        if (currentNode.extraPathsToThisNode != 0):
          numPaths[currentPos] = currentNode.extraPathsToThisNode

      # moving from start edge to playable board
      elif ((nextNode.nodeValue != spaces.BLUE_EDGE or nextNode.nodeValue != spaces.RED_EDGE)
        and (currentNode.nodeValue == spaces.BLUE_EDGE or currentNode.nodeValue == spaces.RED_EDGE)
      ):
        nextNode.setExtraPathsToNode(1)

      else:
        nextNode.setExtraPathsToNode(currentNode.extraPathsToThisNode)

      nodes[pos] = nextNode
      openNodes[pos] = nextNode

    def updateNodeInOpenNodes(pos):
      nonlocal numPaths

      # check if it is a
      if ((nextNode.nodeValue == spaces.BLUE_EDGE or nextNode.nodeValue == spaces.RED_EDGE)
        and (currentNode.nodeValue != spaces.BLUE_EDGE or currentNode.nodeValue != spaces.RED_EDGE)
        and nextNode.g == bestCost
      ):
        if (currentNode.extraPathsToThisNode != 0):

          numPaths[currentPos] = currentNode.extraPathsToThisNode


      # moving from start edge to playable board
      elif ((nextNode.nodeValue != spaces.BLUE_EDGE or nextNode.nodeValue != spaces.RED_EDGE)
        and (currentNode.nodeValue == spaces.BLUE_EDGE or currentNode.nodeValue == spaces.RED_EDGE)
      ):
        nextNode.setExtraPathsToNode(1)

      else:
        openNodes[pos].addExtraPathsToNode(currentNode.extraPathsToThisNode)

    # gotta loop through everything
    while (len(openNodes) > 0):
      currentPos, currentNode = openNodes.popItem()
      closedNodes[currentPos] = currentNode

      adjacentSpaces = self.getAdjacentSpaces(currentPos)
      for nextPos in adjacentSpaces:
        nextNode = nodes[nextPos]

        if (not checkIfBarrier(nextNode) and not closedNodes.hasKey(nextPos)):
          if ((currentNode.pathCost + getCellCost(nextNode)) > bestCost):
            # Too expensive
            pass

          elif (nextPos == endPos):
            # Path Found
            pass

          elif (openNodes.hasKey(nextPos)):
            # In open nodes. check cost compared to this path
            if (nextNode.g > currentNode.g + getCellCost(nextNode)):
              # new path better. Overwrite and set path
              setNodeInOpenNodes(nextPos)

            elif (nextNode.g == currentNode.g + getCellCost(nextNode)):
              # same path same cost. add paths to node
              updateNodeInOpenNodes(nextPos)

          else:
            # not in open nodes
            setNodeInOpenNodes(nextPos)

    # return paths
    #
    total = 0
    ez = []
    while(len(numPaths) > 0):
      i, num = numPaths.popItem()
      ez.append(num)
      total += num
    return total
