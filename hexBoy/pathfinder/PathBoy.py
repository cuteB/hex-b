import copy
from dataclasses import dataclass
from typing import Callable
from hexBoy.hex.HexNode import HexNode
from hexBoy.models.SortedDict import SortedDict
"""
Pathboy more like Slow bois ,amirite
- for real though. need to find a way to save the current seach values
- should be able to keep a hexboard for the boy to remember
"""

'''----------------------------------
Path Finder
----------------------------------'''
@dataclass
class PathBoy:
  getAdjacentSpaces: Callable[[],any]  # function, get adjacent spaces of cell
  getSortValue: Callable  # function to get the value to use for sorting
  checkIfBarrier: Callable
  savedNodes: SortedDict

  def __init__(self,
    gameBoard,
    getAdjacentSpaces,
    barrierCheck,
    getSortValue = None,
  ):
    self.gameBoard = gameBoard
    self.getAdjacentSpaces = getAdjacentSpaces
    self.checkIfBarrier = barrierCheck

    self.initializedSavedNodes = None
    self.savedNodes = self._getInitializedSavedNodes()
    self.initializedSavedNodes = self._getInitializedSavedNodes()

    if (getSortValue == None):
      self.getSortValue = self._defaultGetSortValue
    else:
      self.getSortValue = getSortValue

  # Get the path using the defined pathfinding algorithm
  def findPath(self, startNode, endNode):
    return self.AStar(self.gameBoard.getNodeDict(), startNode, endNode, self.checkIfBarrier)

  def getNumBestPaths(self, startNode, endNode):
    return self.NumBestPaths(self.gameBoard.getNodeDict(), startNode, endNode, self.checkIfBarrier)

  def _defaultGetSortValue(self, item):
    return item[1].hest

  '''---
  AStar
  ---'''
  def AStar(self, nodes, startPos, endPos, checkIfBarrier):
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
            if (nextNode.getPC() > (currentNode.getPC() + nextNode.cost)):
              nextNode.scoreHeuristic(currentPos, currentNode.getPC(), endPos)
              nodes[nextPos] = nextNode
              openNodes[nextPos] = nextNode

          else:
            # Not in open, Score and add to open
            nextNode.scoreHeuristic(
              currentPos,
              currentNode.getPC(),
              endPos
            )
            nodes[nextPos] = nextNode
            openNodes[nextPos] = nextNode

    # after loop
    pathPos = nodes[endPos].parent
    path=[]
    while pathPos != None:
      if not ( # don't include start, end edges
        pathPos[0] == -1 or pathPos[1] == -1
        or pathPos[0] == 11 or pathPos[1] == 11 # TODO change to boardSize
      ):
        path.append(pathPos)
      pathPos = nodes[pathPos].parent

    return path


  def ScorePath(self, path):
    """Score path based on the node's cost"""
    nodes = self.gameBoard.getNodeDict()

    if (len(path) == 0):
      return 10000

    cost = 0
    stepNode = None
    for step in path:
      stepNode = nodes[step]
      cost += stepNode.cost

    return cost

  def _getInitializedSavedNodes(self):
    """Get the First state of the board at the start, save it to save cost"""
    if (self.initializedSavedNodes == None):
      self.initializedSavedNodes = self.scoreBoard()
    return self.initializedSavedNodes

  '''---
  Best paths
  ---'''
  def NumBestPaths(self, nodes, startPos, endPos, checkIfBarrier):
    spaces = HexNode.SpaceTypes
    numPaths = SortedDict()

    winPath = self.AStar(nodes, startPos, endPos, checkIfBarrier)
    bestCost = self.ScorePath(winPath)

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
      nextNode.scoreHeuristic(currentPos, currentNode.getPC(), endPos)
      nonlocal numPaths

      # check if this pos is on the winning edge and moving from a non edge
      # to an end edge
      if ((nextNode.type == spaces.BLUE_EDGE or nextNode.type == spaces.RED_EDGE)
        and (currentNode.type != spaces.BLUE_EDGE or currentNode.type != spaces.RED_EDGE)
        and nextNode.getPC() == bestCost
      ):

        # node is an edge and has the best cost -> is a winning path
        # add paths to the total paths
        if (currentNode.extraPathsToThisNode != 0):
          numPaths[currentPos] = currentNode.extraPathsToThisNode

      # moving from start edge to playable board
      elif ((nextNode.type != spaces.BLUE_EDGE or nextNode.type != spaces.RED_EDGE)
        and (currentNode.type == spaces.BLUE_EDGE or currentNode.type == spaces.RED_EDGE)
      ):
        nextNode.setExtraPathsToNode(1)

      else:
        nextNode.setExtraPathsToNode(currentNode.extraPathsToThisNode)

      nodes[pos] = nextNode
      openNodes[pos] = nextNode

    def updateNodeInOpenNodes(pos):
      nonlocal numPaths

      # check if it is a
      if ((nextNode.type == spaces.BLUE_EDGE or nextNode.type == spaces.RED_EDGE)
        and (currentNode.type != spaces.BLUE_EDGE or currentNode.type != spaces.RED_EDGE)
        and nextNode.getPC() == bestCost
      ):
        if (currentNode.extraPathsToThisNode != 0):
          numPaths[currentPos] = currentNode.extraPathsToThisNode

      # moving from start edge to playable board
      elif ((nextNode.type != spaces.BLUE_EDGE or nextNode.type != spaces.RED_EDGE)
        and (currentNode.type == spaces.BLUE_EDGE or currentNode.type == spaces.RED_EDGE)
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
          if ((currentNode.getPC() + nextNode.cost) > bestCost):
            # Too expensive
            pass

          elif (nextPos == endPos):
            # Path Found
            pass

          elif (openNodes.hasKey(nextPos)):
            # In open nodes. check cost compared to this path
            if (nextNode.getPC() > currentNode.getPC() + nextNode.cost):
              # new path better. Overwrite and set path
              setNodeInOpenNodes(nextPos)

            elif (nextNode.getPC() == currentNode.getPC() + nextNode.cost):
              # same path same cost. add paths to node
              updateNodeInOpenNodes(nextPos)

          else:
            # not in open nodes
            setNodeInOpenNodes(nextPos)

    # return paths
    total = 0
    ez = []
    while(len(numPaths) > 0):
      i, num = numPaths.popItem()
      ez.append(num)
      total += num
    return total

  '''---
  Store Path values
  ---'''
  def scoreBoard(self):
    return SortedDict()

  def scoreMove(self, move, player):
    pass
