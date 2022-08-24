from typing import List

"""
Probs gotta refactor this Kinda sloppy with how everyone uses it
- values are hard to remember what they are
- Way to manage parents and children
- Count Free spaces properly
"""

"""----------------------------------
Hex Node
----------------------------------"""


class HexNode:
    class SpaceTypes:
        EMPTY = 0
        BLUE = 1
        RED = 2
        BLUE_EDGE = 3
        RED_EDGE = 4
        BLUE_START = 5
        RED_START = 6
        BLUE_END = 7
        RED_END = 8

        # List of spaces for each player (others are barriers)
        blueSpaces = [1, 3, 5, 7]
        redSpaces = [2, 4, 6, 8]

    extraPathsToThisNode = None

    # old
    # Gonna use these for the heuristic later
    g = None  # Current Score
    h = None  # Heuristic of this node
    f = None  # Combined g + h

    # newer values
    pos: tuple
    type: int  # Space Type

    # Values and cost
    path: int  # Path to node
    cost: int  # node cost
    dist: int  # Dist to end
    best: int  # current best PCD
    heur: int  # Heuristic to end
    hest: int  # Estimate PCH

    parentPos: tuple
    dads: List[tuple]
    kids: List[tuple]

    def __init__(self, space, pos):
        self.pos = pos
        self.type = space
        self.parent = None  # TODO remove

        self.path = 0
        self.cost = self.getCellCost()
        self.dist = 0
        self.best = 0
        self.heur = 0
        self.hest = 0
        self.dads = []
        self.kids = []

        self.extraPathsToThisNode = 0

        # set the edges to no cost.
        if space == self.SpaceTypes.BLUE_EDGE or space == self.SpaceTypes.RED_EDGE:
            self.cost = 0

    def setSpaceType(self, type):
        self.type = type
        self.cost = self.getCellCost()

    def getPC(self):
        if self.path != None and self.cost != None:
            return self.path + self.cost

    def setParent(self, parent):
        # COMBAK handle parents better. Heuristic uses one dad, many paths can have multiple dads
        self.dads = [parent]

    def setBestPathCost(self, cost):
        self.bestPathCost = cost

    # Score this node and set its parent
    def scoreHeuristic(self, parentPos, pathCost, endPos):
        self.parent = parentPos

        self.path = pathCost
        self.heur = self._getHeuristicEstimate(endPos)
        self.hest = self.path + self.cost + self.heur

    def checkIfEnd(self):
        space = self.type
        return space == self.SpaceTypes.RED_END or space == self.SpaceTypes.BLUE_END

    # TODO This isn't good enough to check if it is a red space.
    # -Only use this in the score function. Scoring a node is never an empty node
    def checkIfBlue(self):

        return self.type in HexNode.SpaceTypes.blueSpaces

    def checkIfRed(self):
        return self.type in HexNodes.SpaceTypes.redSpaces

    def addExtraPathsToNode(self, paths):
        self.extraPathsToThisNode += paths

    def setExtraPathsToNode(self, paths):
        self.extraPathsToThisNode = paths

    def _getHeuristicEstimate(self, endPos):
        """Estimate Distance to End with manhattan"""

        if (
            endPos[1] == 11
        ):  # COMBAK this check is ugly, need another way to check what heuristic to use
            # score blue based on difference in y values
            return abs(endPos[1] - self.pos[1])
        else:
            # score red based on difference in x values
            return abs(endPos[0] - self.pos[0])

    '''---
    Static Functions
    ---'''
    # COMBAK redo these along with the get barriers
    def getCellCost(self):
        type = self.type
        spaces = HexNode.SpaceTypes
        if type == spaces.BLUE_EDGE or type == spaces.RED_EDGE:
            return 0

        elif type == spaces.EMPTY:
            return 1

        elif type == spaces.BLUE or type == spaces.RED:
            return 0

        else:
            return 1

    def checkIfRedBarrier(node):
        space = node.type
        return (
            space in HexNode.SpaceTypes.blueSpaces or space == HexNode.SpaceTypes.EMPTY
        )

    def checkIfBlueBarrier(node):
        space = node.type
        return (
            space in HexNode.SpaceTypes.redSpaces or space == HexNode.SpaceTypes.EMPTY
        )

    def checkIfRedBarrierForAI(node):
        space = node.type
        return space in HexNode.SpaceTypes.blueSpaces

    def checkIfBlueBarrierForAI(node):
        space = node.type
        return space in HexNode.SpaceTypes.redSpaces
