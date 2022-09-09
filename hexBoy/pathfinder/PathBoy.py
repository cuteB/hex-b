from dataclasses import dataclass
from typing import Callable
from xmlrpc.client import APPLICATION_ERROR
from hexBoy.hex.board.HexBoard import Board
from hexBoy.hex.node.HexNode import HexNode, Hex
from hexBoy.models.SortedDict import SortedDict

"""
Pathboy more like Slow bois ,amirite
- for real though. need to find a way to save the current search values
- should be able to keep a hexboard for the boy to remember
"""
# TODO going to use type HexNode for now but will change later for more general use
'''----------------------------------
Path Finder
----------------------------------'''
@dataclass
class PathBoy:
    """Pathfinder. This boy helped me find my own path."""
    _board: Board
    
    _getSortValue: Callable  # function to get the value to use for sorting
    _checkIfBarrier: Callable

    def __init__(
        self,
        board: Board,
        checkIfBarrier: Callable[[Hex], bool],
        getSortValue: Callable[[HexNode], bool] = None,
    ):
        self._board = board
        self._checkIfBarrier = checkIfBarrier 

        if getSortValue == None:
            def _defaultGetSortValue(item: HexNode):
                return item[1].hest
            self._getSortValue = _defaultGetSortValue
        else:
            self._getSortValue = getSortValue

    def findPath(self, startNode: tuple, endNode: tuple):
        return self._AStar(
            self._board.getNodeDict(), startNode, endNode, self._checkIfBarrier
        )

    def scorePath(self, path):
        return self._scorePath(path)

    def findAndScorePath(self, startNode: tuple, endNode: tuple):
        return self._scorePath(self._AStar(
            self._board.getNodeDict(), startNode, endNode, self._checkIfBarrier
        ))

    '''---
    AStar
    ---'''
    def _AStar(self, nodes:dict, startPos: tuple, endPos: tuple, checkIfBarrier:Callable[[tuple], bool]):

        adjacentSpaces = None 
        nextNode = None

        openNodes: SortedDict = SortedDict(getSortValue=self._getSortValue) # nodes that haven't been looked at
        closedNodes: SortedDict = SortedDict() # all nodes that have been looked at already

        currentNode: HexNode  = nodes[startPos] 
        openNodes[currentNode] = currentNode

        # loop while the end hasn't been found
        while currentNode != endPos:
            # All nodes have been looked at, return no path
            if len(openNodes) == 0:
                return []

            # keep looking for path
            # pop off the next node in open and close it
            currentNode, _ = openNodes.popItem() 
            closedNodes[currentNode] = None

            adjacentSpaces = self._board.getAdjacentSpaces(currentNode)
            for nextPos in adjacentSpaces:
                nextNode = nodes[nextPos]

                # Only check if not a barrier and not in closed
                if not checkIfBarrier(nextNode) and not closedNodes.hasKey(nextPos):
                    if openNodes.hasKey(nextPos):
                        # Already in open,
                        # Check if the current value of the node is more than the
                        # cost from the current node would be.
                        if nextNode.getPC() > (currentNode.getPC() + nextNode.cost):
                            nextNode.scoreHeuristic(
                                currentNode, currentNode.getPC(), endPos
                            )
                            nodes[nextPos] = nextNode
                            openNodes[nextPos] = nextNode

                    else:
                        # Not in open, Score and add to open
                        nextNode.scoreHeuristic(currentNode, currentNode.getPC(), endPos)
                        nodes[nextPos] = nextNode
                        openNodes[nextPos] = nextNode

        # after loop
        pathPos = nodes[endPos]
        path = []
        while pathPos != None:
            # if not (  # don't include start, end edges
            #     pathPos[0] == -1
            #     or pathPos[1] == -1
            #     or pathPos[0] == 11
            #     or pathPos[1] == 11  # TODO change to boardSize
            # ):
            #     path.append(pathPos)
            pathPos = nodes[pathPos].parent

        # reverse list
        return list(reversed(path))

    # TODO why this start with capital when findPath doesn't
    def _scorePath(self, path):
        """Score path based on the node's cost"""
        nodes = self.gameBoard.getNodeDict()

        if len(path) == 0:
            return 10000

        cost = 0
        stepNode = None
        for step in path:
            stepNode = nodes[step]
            cost += stepNode.cost

        return cost
