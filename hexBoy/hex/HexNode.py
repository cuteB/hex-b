from dataclasses import dataclass
from typing import List
from __future__ import annotations # Needed because dad: HexNode  is inside the class

"""----------------------------------
Hex 
----------------------------------"""
class Hex(tuple):
    """The Hex, (int, int) \tThe lil guy in charge.""" 
    x: int # First value in tuple
    y: int # Second value in tuple

    def __init__(self, X):
        """The Hex, (int, int) \nCan this indent as well?"""
        tuple.__init__(self)
        self.x = X[0]
        self.y = X[1]

"""----------------------------------
Hex Type
----------------------------------"""
@dataclass
class HexType():
    """Info About the type of hex it is."""
    player: int    # The player that owns this space. 0 neutral, -1 blocked
    hexType: int   # What type of hex this is. Could be different every game. 
    cost: int      # How much this space costs

DefaultHexType = HexType(
    player = 0,
    hexType = 0, # TODO think of a better name than hextype.hextype
    cost = 1
)
    
"""----------------------------------
Hex Node
----------------------------------"""
class HexNode(Hex):
    """Hex with a bunch of values important to the game board and path finding"""

    # Hex Type
    _type: HexType 

    # Values and cost for path finding
    _path: int  # P: Path to node cost
    _cost: int  # C: node cost
    _dist: int  # D: Dist to end cost
    _heur: int  # H: Heuristic to end
    _best: int  # current best PCD
    _hest: int  # Estimate PCH

    # family
    _dads: List[HexNode]  # Parent(s) of the node. Could have been moms too i guess. 

    def __init__(self, X, xType: HexType = DefaultHexType):
        Hex.__init__(self, X)
        
        self._type = xType

        self._path = 0
        self._cost = self.xType.cost
        self._dist = 0
        self._best = 0
        self._heur = 0
        self._hest = 0

        self._dads = []

    '''---
    Public Functions
    ---'''
    def setHexType(self, xType: HexType) -> None:
        """Set HexType and overwrite cost"""
        self.xType = xType
        self.cost = xType.cost()

    def getHexType(self) -> HexType:
        """Get HexType (do I really need a comment for this)"""
        return self.xType

    def getPC(self) -> int:
        "Get path cost to node + cost of node"
        return self.path + self.cost

    def getParent(self) -> HexNode:
        """Get single parent of the node, First parent if it has many"""
        if (len(self._dads) > 0):
            return self._dads[0]
        else: 
            return None

    def getCost(self) -> int:
        """Get the current cost of the cell"""
        return self._cost
