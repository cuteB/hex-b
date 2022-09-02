from typing import List
from dataclasses import dataclass
from hexBoy.hex.node.HexNode import HexNode, Hex
from hexBoy.hex.game.HexGameRules import HexGameRules
from abc import ABC, abstractmethod

'''----------------------------------
Board
----------------------------------'''
@dataclass
class Board(ABC):
    _boardNodeDict: dict # dict<

    @abstractmethod
    def getNodeDict(self) -> dict:
        """Get the board node dict"""

    @abstractmethod
    def setNodeDict(self, dict: dict) -> None:
        """Set the board node dict"""

    @abstractmethod
    def isSpaceWithinBounds(self, cell: tuple) -> bool:
        """Check if space is in the playable area"""

    @abstractmethod
    def getAdjacentSpaces(self, cell: tuple) -> List[tuple]:
        """Return spaces that are beside the cell"""

'''----------------------------------
Hexagon Board
----------------------------------'''
class HexagonBoard(Board):
    """Generic board of hexagons"""

    # Uncle Arjan said "no non-abstract methods in abstract classes"
    def getNodeDict(self) -> dict:
        """Return the board node dict"""
        return self._boardNodeDict

    def setNodeDict(self, dict) -> None: 
        """Set the board dict"""
        self._boardNodeDict = dict

    def isSpaceWithinBounds(self, cell) -> bool:
        """"Check if the pos is within the playable space"""
        return (cell in dict)
    
    def getAdjacentSpaces(self, cell: tuple) -> List[tuple]:
        """Get the Hexes touching the given cell"""
        # Checkout /wiki/hex/Board.md for the board with coordinates
        (x,y) = cell

        # eg for cell             (1,1)
        potentialSpaces = [
            (x, y - 1),         # (1,0) up
            (x, y + 1),         # (1,2) down
            (x - 1, y),         # (0,1) left
            (x + 1, y),         # (2,1) right
            (x - 1, y + 1),     # (0,2) down+left
            (x + 1, y - 1),     # (2,0) up+right
        ]

        # validate the potential spaces and return the adjacent spaces
        adjacentSpaces = []
        for space in potentialSpaces:
            if self.isSpaceWithinBounds(space):
                adjacentSpaces.append(space)

        return adjacentSpaces

'''----------------------------------
Hex Board
----------------------------------'''
class HexBoard(HexagonBoard): 
    """Official Hex Game Board. 11x11 board of hexagons"""

    boardSize: int  # size of the board

    _boardNodeDict: dict # dict<Hex -> HexNode>
    _initializedBoardDict: dict # Copy of initial boardNodeDict
    _moveHistory: List[tuple(Hex, int)] 
    _blueEndZone: List[Hex]
    _redEndZone: List[Hex]

    def __init__(self):
        self.boardSize = 11 # Always 11. 

        self._boardNodeDict = self._initGameBoard()
        self._moveHistory = [] 

    def _initGameBoard(self) -> dict:
        """Initialize the starting game board and save for when the game resets, save a list of the  edges for each player"""
        dict = {}

        # initialize playing spaces
        for x in range(self.boardSize):
            for y in range(self.boardSize):
                dict[Hex((x, y))] = HexNode((x, y), HexGameRules.empty.hex)

        # Initialize edges in dict
        # blue edge
        for x in range(self.boardSize):
            self.blueEndZone.append(Hex((x, -1)))
            self.blueEndZone.append(Hex((x, 11)))
            dict[Hex((x, -1))] = HexNode((x, -1), HexGameRules.blue.edge)
            dict[Hex((x, 11))] = HexNode((x, 11), HexGameRules.blue.edge)

        # red edge
        for y in range(self.boardSize):
            self.redEndZone.append(Hex((-1, y)))
            self.redEndZone.append(Hex((11, y)))
            dict[Hex((-1, y))] = HexNode((-1, y), HexGameRules.red.edge)
            dict[Hex((11, y))] = HexNode((11, y), HexGameRules.red.edge)

        self._initializedBoardDict = dict
        return dict

    '''---
    Public
    ---'''
    def validateMove(self, X: Hex) -> bool: 
        """Check if the given cell is a valid move. Space in Empty and on the board"""
        return (
            X != None
            and self.isSpaceWithinBounds(X)
            and self._boardNodeDict[X].getHexType() == HexGameRules.empty.hex 
        )

    def makeMove(self, player: int, X: Hex) -> None:
        """Make a move on the board and save it in history"""
        self._moveHistory.append((X, player))
        self.boardDict[X].setHexType(HexGameRules.getPlayerHex(player))

    def resetGameBoard(self) -> None: # TODO move to HexBoard, rename resetGameBoard
        """Reset the board and move history"""
        self.boardDict = self._initializedBoardDict
        self._moveHistory = []

    def getPlayerMoves(self, player: int) -> List[(Hex, int)]:
        """Look at the move history and return a player's moves"""
        playerMoves = []
        for i in range(len(self._moveHistory)):
            if self._moveHistory[i][1] == player:
                playerMoves.append(self._moveHistory[i][0])

        return playerMoves

    def getPlayerEndZone(self, player: int) -> List[Hex]:
        """Get the end zone hexes of the player"""
        if(player == 1): 
            return self._blueEndZone
        else:
            return self._redEndZone
