from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

from hexBoy.hex.game.HexGameRules import HexGameRules
from hexBoy.hex.node.HexNode import HexNode, Hex

'''----------------------------------
Board
----------------------------------'''
class Board(ABC):
    """Abstract Board"""
    _boardNodeDict: Dict[tuple, tuple]

    @abstractmethod
    def getNodeDict(self) -> Dict[tuple, tuple]:
        """Get the board node dict"""

    @abstractmethod
    def setNodeDict(self, dict: Dict[tuple, tuple]) -> None:
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
    # Override
    def getNodeDict(self) -> Dict[Hex, HexNode]:
        return self._boardNodeDict

    # Override
    def setNodeDict(self, dict) -> None: 
        self._boardNodeDict = dict

    # Override
    def isSpaceWithinBounds(self, cell) -> bool:
        return (cell in self._boardNodeDict)
    
    # Override
    def getAdjacentSpaces(self, cell: tuple) -> List[tuple]:
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
        return [
            space
            for space in potentialSpaces
            if self.isSpaceWithinBounds(space)
        ]

'''----------------------------------
Hex Board
----------------------------------'''
class HexBoard(HexagonBoard): 
    """Official Hex Game Board. 11x11 board of hexagons"""

    boardSize: int  # size of the board
    _boardNodeDict: Dict[Hex, HexNode] 

    # _initializedBoardDict: dict # Copy of initial boardNodeDict
    _moveHistory: List[Tuple[int, Hex]]
    _blueEndZone: List[Hex]
    _redEndZone: List[Hex]

    def __init__(self):
        self.boardSize = 11 # Always 11. 

        self._boardNodeDict = self._initGameBoard()
        self._moveHistory = []

    def _initGameBoard(self) -> Dict[Hex, HexNode]:
        """Initialize the starting game board and save for when the game resets"""

        # Run every time. Saving this has pointer issues. Could probs deep copy
        dict = {}
        self._blueEndZone = [(x,y) for x in range(self.boardSize) for y in [-1,11]]
        self._redEndZone = [(x,y) for y in range(self.boardSize) for x in [-1,11]]

        # initialize the dict with comprehension
        dict = {
            Hex((x,y)): HexNode((x,y)).initHexType(HexGameRules.blue.edge) if y == -1 or y == 11
            else HexNode((x,y)).initHexType(HexGameRules.red.edge) if x == -1 or x == 11
            else HexNode((x,y)).initHexType(HexGameRules.empty.hex)
            for x in range(-1, self.boardSize + 1) for y in range(-1, self.boardSize + 1)
            if (x,y) not in [(11,11), (-1,-1), (-1,11), (11,-1)] # ignore the 4 edge corners 
        }
        
        return dict # need to return the dict instead of just setting it here.

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

        self._moveHistory.append((player, X))
        self._boardNodeDict[X].setHexType(HexGameRules.getPlayerHex(player))

    def resetGameBoard(self) -> None:
        """Reset the board and move history"""

        self._boardNodeDict = self._initGameBoard()
        self._moveHistory = []

    def getPlayerMoves(self, player: int) -> List[Hex]:
        """Look at the move history and return a player's moves"""
        # move (player, move)
        return [
            m[1] 
            for m in self._moveHistory 
            if m[0] == player
        ]

    def getMoveHistory(self) -> List[Tuple[int,Hex]]:
        """Get the move history of the current game"""

        return self._moveHistory

    def getPlayerEndZone(self, player: int) -> List[Hex]:
        """Get the end zone hexes of the player"""

        if (player == 1): 
            return self._blueEndZone
        else:
            return self._redEndZone
