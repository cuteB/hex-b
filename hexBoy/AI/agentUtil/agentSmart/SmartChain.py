from typing import List
from hexBoy.models.SortedDict import SortedDict
from hexBoy.hex.node.HexNode import Hex
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.game.HexGameRules import HexGameRules, HexPlayerInfo
from hexBoy.AI.agentUtil.board.GetConnections import GetConnections
from hexBoy.AI.agentUtil.board.GetStrongMoves import GetStrongMoves
from hexBoy.AI.agentUtil.pathfinder.TrimPath import TrimEdgesFromPath
from hexBoy.pathfinder.PathBoy import PathBoy

'''----------------------------------
Smart Chain
----------------------------------'''
class SmartChain():
    """A chain that links hexes that have a connection on a board"""
    
    _gameBoard: HexBoard
    _playerInfo: HexPlayerInfo = None

    _pf: PathBoy
    _linkedDict: SortedDict = None
    _connections: List[Hex] = None
    _startPos: Hex = None
    _endPos: Hex = None
    _startDist: int = None
    _endDist: int = None
    _length: int = None

    def __init__(self, player: int, board: HexBoard):
        self._gameBoard = board
        self._playerInfo = HexGameRules.getPlayerInfo(player)

        self._connections = []
        self._linkedDict = SortedDict()
        self._length = 0
        
        self._pf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._playerInfo.player), 
            HexGameRules.getHeuristicFunc(self._playerInfo.player)
        )

        # update chain based on board
        self.updateChain()

    '''---
    Public
    ---'''
    def updateChain(self) -> None:
        """Look at the board and get the chain"""

        playerMoves = self._gameBoard.getPlayerMoves(self._playerInfo.player)
        nMoves = len(playerMoves)
        self._connections = []
        # No moves
        if (nMoves == 0):
            return
        
        (weakConnections, strongConnections) = GetConnections(self._gameBoard, self._playerInfo.player)
        bestPath = TrimEdgesFromPath(self._pf.findPath(self._playerInfo.start, self._playerInfo.end))
        # count player moves in path
        nMoves = 0
        for node in bestPath:
            if (node in playerMoves):
                nMoves += 1

        lastNode = None
        lenBestPath = len(bestPath)
        length = 0
        iMove = 0 # capture move index
        i = 0
        for X in bestPath:
            # Player Move
            if (X in playerMoves):
                iMove += 1
                length += 1
                if (iMove == 1): 
                    # first move
                    self._startPos = X
                    self._startDist = i
                    lastNode = X
                
                if (iMove == nMoves):
                    # last move
                    self._endPos = X
                    self._endDist = lenBestPath - i - 1
                    self._linkedDict[lastNode] = X
                    lastNode = X

                if (iMove != 1 and iMove != nMoves):
                    # middle move
                    self._linkedDict[lastNode] = X
                    lastNode = X

            # Weak Connection
            elif (X in weakConnections):
                length += 1
                self._connections.append(X)

            elif (X in strongConnections):
                length += 1
                self._connections.append(X)

                adjacentHexes = self._gameBoard.getAdjacentSpaces(X)
                for aX in adjacentHexes:
                    if aX in strongConnections:
                        self._connections.append(aX)

            i += 1

        # finish up 
        if (lastNode != None):
            self._linkedDict[lastNode] = None
        self._length = length

    def getStartPotentialMoves(self) -> list:
        """Get Potential moves for the start pos (not validated)"""

        (x,y) = self._startPos
        strongMoves = GetStrongMoves(self._gameBoard, self._playerInfo.player)

        pMoves = []
        pStrongMoves = []
        if (self._playerInfo.player == 1):
            # blue
            pMoves = self._gameBoard.getAdjacentSpaces(self._startPos)
            pStrongMoves = [
                (x-1, y-1),
                (x+2, y-1),
                (x+1, y-2)
            ]
        
        else:
            # red
            pMoves = self._gameBoard.getAdjacentSpaces(self._startPos)
            pStrongMoves = [   
                (x-1, y-1),
                (x-1, y+2),
                (x-2, y+1)
            ]

        potentialMoves = []
        for m in pMoves:
            if (self._gameBoard.validateMove(m) and m not in self._connections):
                potentialMoves.append(m)

        for m in pStrongMoves:
            if (m in strongMoves and m not in self._connections):
                potentialMoves.append(m)
                
        return potentialMoves

    def getEndPotentialMoves(self) -> list:
        """Get Potential moves for the end pos"""
        (x,y) = self._endPos
        strongMoves = GetStrongMoves(self._gameBoard, self._playerInfo.player)

        pMoves = []
        if (self._playerInfo.player == 1):
            # blue
            pMoves = self._gameBoard.getAdjacentSpaces(self._endPos)
            pStrongMoves = [   
                (x-2, y+1),
                (x+1, y+1),
                (x-1, y+2),
            ]
        
        else:
            # red
            pMoves = self._gameBoard.getAdjacentSpaces(self._endPos)
            pStrongMoves = [   
                (x+1, y-2),
                (x+1, y+1),
                (x+2, y-1),
            ]

        potentialMoves = []
        for m in pMoves:
            if (self._gameBoard.validateMove(m) and m not in self._connections):
                potentialMoves.append(m)

        for m in pStrongMoves:
            if (m in strongMoves and m not in self._connections):
                potentialMoves.append(m)
                
        return potentialMoves

    def getPotentialMoves(self) -> list:
        """Get Moves that will extend the chain to the end"""

        # For now just going to return the three strong moves closer to the closest edge and the two short moves. (for both start and end)
        startMoves = []
        endMoves = []
        if (self._startPos and self._startDist > 1):
            startMoves = self.getStartPotentialMoves()

        if (self._endPos and self._endDist > 1):
            endMoves = self.getEndPotentialMoves()

        return [*startMoves, *endMoves]

    def printChain(self) -> None:
        """Print the nodes in the chain"""
        chain = []
        
        if self._length > 0:
            X = self._startPos
            while( X != None):
                chain.append(X)
                X = self._linkedDict[X]

        print(chain)

    def getDistToEndZone(self, X) -> int:
        """"Get distance to closest player endZone (i think this exists somewhere)"""

        if (self._playerInfo.player == 1):
            # blue, compare y
            val = X[1]
        else:
            # red, compare x
            val = X[0]

        # assume board size 11
        if (val <= 5):
            return val + 1
        else:
            return 11 - val

    def getLength(self) -> int:
        """Get length of the chain"""

        return self._length

    def getStartDist(self) -> int:
        """Get distance of the start to the starting edge"""

        return self._startDist

    def getEndDist(self) -> int:
        """Get distance of the end to the ending edge"""

        return self._endDist
    
    def getConnections(self) -> List[Hex]:
        """Get connections used in the chain"""

        return self._connections

    def getStartPos(self) -> Hex:
        """Get the starting hex of the chain"""

        return self._startPos

    def getEndPos(self) -> Hex:
        """Get the ending hex of the chain"""

        return self._endPos