from __future__ import annotations # Needed because dad: HexNode  is inside the class
from dataclasses import dataclass
from typing import List

'''----------------------------------
Hex 
----------------------------------'''
class Hex(tuple):
    """The Hex, tuple(int, int) 

    > The lil guy in charge.""" 

    def __init__(self, X):
        """The Hex, (int, int) """
        tuple.__init__(self)

'''----------------------------------
Hex Type
----------------------------------'''
@dataclass
class HexType():
    """Info About the type of hex it is."""

    player: int    # The player that owns this space. 0 neutral, -1 blocked
    xType: int   # What type of hex this is. Could be different every game. 
    cost: int      # How much this space costs

DefaultHexType = HexType(
    player = 0,
    xType = 1,
    cost = 1
)

'''----------------------------------
Hex Node
----------------------------------'''
class HexNode(Hex):
    """Hex with a bunch of values important to the game board and path finding"""

    # Note: Might want another class 'Node' with the PCD values and HexNode inherit from Hex and Node. I would like the pathfinder to not have to be reliant on HexNode

    # Hex Type
    _type: HexType 

    # Values and cost for path finding
    _path: int  # P: Path to node cost
    _cost: int  # C: node cost
    _dist: int  # D: Dist to end cost
    _heur: int  # H: Heuristic to end

    # family
    _dads: List[HexNode]  # Parent(s) of the node. Could have been moms too i guess. 
    _sons: List[HexNode]  # Kid(s) of the node. Because parents only care about their best kids

    def __init__(self, X):
        Hex.__init__(self, X)
        
        self._type = DefaultHexType

        self._path = 0
        self._cost = self._type.cost
        self._dist = 0
        self._heur = 0

        self._dads = []
        self._sons = []

    '''---
    Public Functions
    ---'''
    def getHexType(self) -> HexType:
        """Get HexType (do I really need a comment for this)"""
        return self._type

    def setHexType(self, xType: HexType) -> None:
        """Set HexType and overwrite cost of the node"""
        self._type = xType
        self._cost = xType.cost

    def initHexType(self, xType: HexType) -> HexNode:
        """Set HexType and return the hex for a one liner init"""
        self.setHexType(xType)
        return self

    def getPath(self) -> int:
        """Get the cost of the path that gets to this node"""
        return self._path

    def setPath(self, path: int) -> None:
        """Set the path cost"""
        self._path = path

    def getCost(self) -> int:
        """Get the current cost of the cell"""
        return self._cost

    def getDist(self) -> int:
        """Get the distance to the end from this node"""
        return self._dist

    def setDist(self, dist: int) -> None:
        """Set the distance from the node"""
        self._dist = dist

    def getHeur(self) -> int:
        """Get the heuristic from the node"""
        return self._heur

    def setHeur(self, heur: int) -> None:
        """Set the heuristic from the node"""
        self._heur = heur

    def getHest(self) -> int:
        """Get the Estimate total cost of the path using the node with the Heuristic"""
        # return self._hest
        return self._path + self._cost + self._heur

    def getBest(self) -> int:
        """Get Best Cost of the nodes entire path"""
        return self._path + self._cost + self._dist

    def getPC(self) -> int:
        "Get path cost to node + cost of node"
        return self._path + self._cost

    def getParent(self) -> HexNode:
        """Get single parent of the node, First parent if it has many"""
        if (len(self._dads) > 0):
            return self._dads[0]
        else: 
            return None

    def setParent(self, parent: HexNode) -> None:
        """Set a single parent to the node"""
        self._dads = [parent]
