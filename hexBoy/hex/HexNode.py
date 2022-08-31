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
class HexNode: # TODO Can I inherit a tuple? I think that would be awesome. 
    class SpaceTypes: # TODO rename to HexType
        # TODO I think I want to come back to the types. I want this to be a more complex object rather than ints. 
        # - Want costs and get barriers inside this object
        # TODO I almost want an "rules" object with all of this: Hex types, start pos and all that jazz. Each player has an endzone, moves, start and end positions
        EMPTY = 0
        BLUE = 1
        RED = 2
        BLUE_EDGE = 3
        RED_EDGE = 4
        # TODO delete, start and end aren't used anywhere
        BLUE_START = 5
        RED_START = 6
        BLUE_END = 7
        RED_END = 8

        # List of spaces for each player (others are barriers)
        blueSpaces = [1, 3, 5, 7]
        redSpaces = [2, 4, 6, 8]

    extraPathsToThisNode = None

    # old # TODO I think these can be deleted. 
    # Gonna use these for the heuristic later
    g = None  # Current Score
    h = None  # Heuristic of this node
    f = None  # Combined g + h

    # newer values
    pos: tuple
    type: int  # Space Type

    # Values and cost
    path: int  # P: Path to node cost
    cost: int  # C: node cost
    dist: int  # D: Dist to end cost
    heur: int  # H: Heuristic to end
    best: int  # current best PCD
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

    def setSpaceType(self, type): # TODO rename
        self.type = type
        self.cost = self.getCellCost()

    def getPC(self):
        # TODO this can return None
        if self.path != None and self.cost != None:
            return self.path + self.cost

    def setParent(self, parent):
        # TODO Delete, not used
        # COMBAK handle parents better. Heuristic uses one dad, many paths can have multiple dads
        self.dads = [parent]

    def setBestPathCost(self, cost):
        # TODO delete, not used
        self.bestPathCost = cost

    # Score this node and set its parent
    def scoreHeuristic(self, parentPos, pathCost, endPos):
        self.parent = parentPos

        self.path = pathCost
        self.heur = self._getHeuristicEstimate(endPos)
        self.hest = self.path + self.cost + self.heur

    def checkIfEnd(self):
        # TODO delete, not used
        space = self.type
        return space == self.SpaceTypes.RED_END or space == self.SpaceTypes.BLUE_END

    # TODO This isn't good enough to check if it is a red space.
    # -Only use this in the score function. Scoring a node is never an empty node
    def checkIfBlue(self): # TODO Delete, not used
        return self.type in HexNode.SpaceTypes.blueSpaces

    def checkIfRed(self): # TODO delete, not used
        return self.type in HexNode.SpaceTypes.redSpaces

    def addExtraPathsToNode(self, paths):
        self.extraPathsToThisNode += paths

    def setExtraPathsToNode(self, paths):
        self.extraPathsToThisNode = paths

    def _getHeuristicEstimate(self, endPos):
        """Estimate Distance to End with manhattan"""

        if (
            endPos[1] == 11
        ):  # TODO this check is ugly, need another way to check what heuristic to use.
            # score blue based on difference in y values
            return abs(endPos[1] - self.pos[1])
        else:
            # score red based on difference in x values
            return abs(endPos[0] - self.pos[0])

    '''---
    Static Functions
    ---'''
    # COMBAK redo these along with the get barriers
    # TODO move most of the logic into HexType. 
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

    # TODO remove checkIfRedBarrier and checkIfBlueBarrier and change into a single function. Need the first two for the HexGame winning path func
    def checkIfRedBarrier(node): # TODO delete
        space = node.type
        return (
            space in HexNode.SpaceTypes.blueSpaces or space == HexNode.SpaceTypes.EMPTY
        )

    def checkIfBlueBarrier(node): # TODO delete
        space = node.type
        return (
            space in HexNode.SpaceTypes.redSpaces or space == HexNode.SpaceTypes.EMPTY
        )

    def checkIfRedBarrierForAI(node): # TODO delete
        space = node.type
        return space in HexNode.SpaceTypes.blueSpaces

    def checkIfBlueBarrierForAI(node): # TODO delete
        space = node.type
        return space in HexNode.SpaceTypes.redSpaces
