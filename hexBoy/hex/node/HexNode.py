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

    # paths to and from node
    _pathsToNode: int
    _pathsFromNode: int 

    def __init__(self, X):
        Hex.__init__(self, X)
        
        self._type = DefaultHexType

        self._path = 0
        self._cost = self._type.cost
        self._dist = 0
        self._heur = 0

        self._dads = []
        self._sons = []

        self._pathsToNode = 0
        self._pathsFromNode = 0

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
        return self._path + self._cost + self._heur

    def getBest(self) -> int:
        """Get Best Cost of the nodes entire path"""
        return self._path + self._cost + self._dist

    def getPC(self) -> int:
        "Get path cost to node + cost of node"
        return self._path + self._cost

    def getCD(self) -> int:
        """Get cost of node + dist to end"""
        return self._cost + self._dist

    def getDad(self) -> HexNode:
        """Get single dad of the node, First dad if it has many"""
        if (len(self._dads) > 0):
            return self._dads[0]
        else: 
            return None

    def getDads(self) -> List[HexNode]:
        """Get all dads of the node"""
        return self._dads

    def setDad(self, dad: HexNode) -> None:
        """Set a single dad to the node"""
        self._dads = [dad]

    def setDads(self, dads: List[HexNode]) -> None:
        """Set dads from list"""
        self._dads = dads

    def addDad(self, dad: HexNode) -> None:
        """Add a dad to the node"""
        if not dad in self._dads:
            self._dads.append(dad)

    def delDad(self, dad: HexNode) -> None:
        """Delete a dad from the node if it exists"""
        if dad in self._dads:
            self._dads.remove(dad) 
            self.updatePathsToNodeWithDads()

    def getSon(self) -> HexNode:
        """Get single son of the node, First son if it has many"""
        if (len(self._sons) > 0):
            return self._sons[0]
        else: 
            return None

    def setSon(self, son: HexNode) -> None:
        """Set a single son to the node"""
        self._sons = [son]

    def setSons(self, sons: List[HexNode]) -> None:
        """Set sons from list"""
        self._sons = sons

    def addSon(self, son: HexNode) -> None:
        """Add a son to the node"""
        if not son in self._sons:
            self._sons.append(son)
    
    def getSons(self) -> List[HexNode]:
        """Get all sons of the node"""
        return self._sons

    def delSon(self, son: HexNode) -> None:
        """Delete a son from the node if it exists"""
        if son in self._sons:
            self._sons.remove(son) 
            self.updatePathsFromNodeWithSons()

    def setPathsToNode(self, n: int) -> None:
        """Set the paths to node"""
        self._pathsToNode = n
    
    def updatePathsToNodeWithDads(self) -> None:
        """Update the paths to node by looking at dads"""
        dads: List[HexNode] = self.getDads()
        pathsToNode = 0
        for d in dads:
            pathsToNode += d.getPathsToNode()

        self.setPathsToNode(pathsToNode)

    def getPathsToNode(self) -> int:
        """Get the paths to node"""
        return self._pathsToNode

    def setPathsFromNode(self, n: int) -> None:
        """Set the paths from node"""
        self._pathsFromNode = n

    def updatePathsFromNodeWithSons(self) -> None:
        """Update the paths from node by looking at sons"""
        sons: List[HexNode] = self.getSons()
        pathsFromNode = 0
        for s in sons:
            pathsFromNode += s.getPathsFromNode()

        self.setPathsFromNode(pathsFromNode)

    def getPathsFromNode(self) -> int:
        """Get the paths from node"""
        return self._pathsFromNode
        