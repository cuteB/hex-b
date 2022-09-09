from dataclasses import dataclass
from typing import Callable, Dict
from hexBoy.hex.board.HexBoard import Board
from hexBoy.hex.node.HexNode import HexNode, Hex
from hexBoy.models.SortedDict import SortedDict

'''----------------------------------
Path Finder
----------------------------------'''
@dataclass
class PathBoy:
    """Pathfinder. This boy helped me find my own path."""
    _board: Board
    
    # Note: going to use type HexNode for now but will change later for more general use
    _heuristicFunc: Callable[[HexNode], int]  # Heuristic function for A*
    _checkIfBarrier: Callable[[Hex], bool]    
    _getSortValue: Callable[[HexNode], bool]  # SortedDict function

    def __init__(
        self,
        board: Board,
        checkIfBarrier: Callable[[Hex], bool],
        heuristicFunc: Callable[[HexNode], int], 
        getSortValue: Callable[[HexNode], bool] = None,
    ):
        self._board = board
        self._heuristicFunc = heuristicFunc
        self._checkIfBarrier = checkIfBarrier

        if getSortValue == None:
            def _defaultGetSortValue(item: HexNode):
                return item[1].hest
            self._getSortValue = _defaultGetSortValue
        else:
            self._getSortValue = getSortValue

    def findPath(self, startNode: tuple, endNode: tuple):
        """Find path from start to end positions"""

        return self._AStar(
            startNode, endNode, self._checkIfBarrier
        )

    def scorePath(self, path):
        """Score path cost of a path"""

        return self._scorePath(path)

    def findAndScorePath(self, startNode: tuple, endNode: tuple):
        """Find path and return the score"""

        return self._scorePath(self._AStar(
            startNode, endNode, self._checkIfBarrier
        ))

    '''---
    AStar
    ---'''
    def _AStar(self, startPos: tuple, endPos: tuple, checkIfBarrier:Callable[[tuple], bool]):
        """A* path finding algorithm"""

        nodes: Dict[Hex, HexNode] = self._board.getNodeDict()
        adjacentSpaces = None 
        nextNode = None

        openNodes: SortedDict = SortedDict(getSortValue=self._getSortValue)
        closedNodes: SortedDict = SortedDict()

        currentNode: HexNode  = nodes[startPos] 
        openNodes[currentNode] = currentNode

        def scoreHeuristic(node: HexNode, parent: HexNode, pathCost: int):
            """Score Node: set parent, path and heuristic value"""

            node.setParent(parent)
            node.setPath(pathCost)
            node.setHeur(self._heuristicFunc(node))

        # loop while the end hasn't been found
        while currentNode != endPos:
            # All nodes have been looked at, return no path
            if len(openNodes) == 0:
                return []

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
                        if nextNode.getPC() > (currentNode.getPC() + nextNode.getCost()):
                            scoreHeuristic(nextNode, currentNode, currentNode.getPC())
                            nodes[nextNode] = nextNode
                            openNodes[nextNode] = nextNode

                    else:
                        # Not in open, Score and add to open
                        scoreHeuristic(nextNode, currentNode, currentNode.getPC())
                        nodes[nextNode] = nextNode
                        openNodes[nextNode] = nextNode

        # after loop. Turn linked nodes into list
        pathPos = nodes[endPos]
        path = []
        while pathPos != None:
            path.append(pathPos)
            pathPos = nodes[pathPos].getParent()
        
        # reverse list
        return list(reversed(path))

    def _scorePath(self, path):
        """Score path based on the node's cost"""
        
        nodes = self._board.getNodeDict()

        if len(path) == 0: # Maybe change to None instead of a big number
            return 10000

        cost = 0
        stepNode = None
        for step in path:
            stepNode = nodes[step]
            cost += stepNode.getCost()

        return cost
