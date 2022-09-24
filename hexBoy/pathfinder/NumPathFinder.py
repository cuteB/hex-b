from typing import Callable

from hexBoy.hex.board.HexBoard import Board
from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.node.HexNode import HexNode
from hexBoy.models.SortedDict import SortedDict

# COMEBACK and do this

class NumPathFinder(PathBoy):

    def __init__(
        self,
        board: Board,
        checkIfBarrier: Callable[[tuple], bool],
        getSortValue: Callable[[any], bool] = None,
    ):
        super(PathBoy, self)

    def getNumBestPaths(self, startNode: tuple, endNode):
        return self._numBestPaths(
             startNode, endNode, self._checkIfBarrier
        )

    '''---
    Best paths
    ---'''
    def _numBestPaths(self, nodes, startPos, endPos, checkIfBarrier):
        nodes = self._board.getNodeDict(),
        spaces = HexNode.SpaceTypes
        numPaths = SortedDict()

        winPath = self._AStar(startPos, endPos)
        bestCost = self.scorePath(winPath)

        openNodes = SortedDict(getSortValue=self.getSortValue)
        closedNodes = SortedDict()
        endNodes = SortedDict()  # nodes to add up to get the number of paths

        # add starting position to pop off
        currentPos = startPos # maybe rename Pos to Hex
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
            if (
                (nextNode.type == spaces.BLUE_EDGE or nextNode.type == spaces.RED_EDGE)
                and (
                    currentNode.type != spaces.BLUE_EDGE
                    or currentNode.type != spaces.RED_EDGE
                )
                and nextNode.getPC() == bestCost
            ):
                # node is an edge and has the best cost -> is a winning path
                # add paths to the total paths
                if currentNode.extraPathsToThisNode != 0:
                    numPaths[currentPos] = currentNode.extraPathsToThisNode

            # moving from start edge to playable board
            elif (
                nextNode.type != spaces.BLUE_EDGE or nextNode.type != spaces.RED_EDGE
            ) and (
                currentNode.type == spaces.BLUE_EDGE
                or currentNode.type == spaces.RED_EDGE
            ):
                nextNode.setExtraPathsToNode(1)

            else:
                nextNode.setExtraPathsToNode(currentNode.extraPathsToThisNode)

            nodes[pos] = nextNode
            openNodes[pos] = nextNode

        def updateNodeInOpenNodes(pos):
            nonlocal numPaths

            # check if it is a # check if it is a what?
            if (
                (nextNode.type == spaces.BLUE_EDGE or nextNode.type == spaces.RED_EDGE)
                and (
                    currentNode.type != spaces.BLUE_EDGE
                    or currentNode.type != spaces.RED_EDGE
                )
                and nextNode.getPC() == bestCost
            ):
                if currentNode.extraPathsToThisNode != 0:
                    numPaths[currentPos] = currentNode.extraPathsToThisNode

            # moving from start edge to playable board
            elif (
                nextNode.type != spaces.BLUE_EDGE or nextNode.type != spaces.RED_EDGE
            ) and (
                currentNode.type == spaces.BLUE_EDGE
                or currentNode.type == spaces.RED_EDGE
            ):
                nextNode.setExtraPathsToNode(1)

            else:
                openNodes[pos].addExtraPathsToNode(currentNode.extraPathsToThisNode)

        # gotta loop through everything
        while len(openNodes) > 0:
            currentNode = openNodes.popKey()
            closedNodes[currentNode] = None

            adjacentSpaces = self.getAdjacentSpaces(currentNode)
            for nextPos in adjacentSpaces:
                nextNode = nodes[nextPos]

                if not checkIfBarrier(nextNode) and not closedNodes.hasKey(nextPos):
                    if (currentNode.getPC() + nextNode.cost) > bestCost:
                        # Too expensive
                        pass

                    elif nextPos == endPos:
                        # Path Found
                        pass

                    elif openNodes.hasKey(nextPos):
                        # In open nodes. check cost compared to this path
                        if nextNode.getPC() > currentNode.getPC() + nextNode.cost:
                            # new path better. Overwrite and set path
                            setNodeInOpenNodes(nextPos)

                        elif nextNode.getPC() == currentNode.getPC() + nextNode.cost:
                            # same path same cost. add paths to node
                            updateNodeInOpenNodes(nextPos)

                    else:
                        # not in open nodes
                        setNodeInOpenNodes(nextPos)

        # return paths
        total = 0
        ez = [] #  remove if not used
        while len(numPaths) > 0:
            num = numPaths.pop()
            ez.append(num)
            total += num
        return total
        