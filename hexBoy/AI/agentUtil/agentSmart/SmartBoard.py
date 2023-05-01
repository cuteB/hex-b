from typing import Callable, Dict, List, Tuple
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.game.HexGameRules import HexPlayerInfo, HexGameRules
from hexBoy.hex.node.HexNode import Hex, HexNode
from hexBoy.models.SortedDict import SortedDict

# TODO I probably want this as a path finder

class SmartBoard(HexBoard):
    """Board that keeps track of the number of best paths to the goal"""

    _playerInfo: HexPlayerInfo
    _heuristic: Callable[[Hex, Hex], int]

    def __init__(self, player: int):
        super(HexBoard, self)

        self._playerInfo = HexGameRules.getPlayerInfo(player)
        self._heuristic = HexGameRules.getHeuristicFunc(player)

    # Override
    def _initGameBoard(self) -> Dict[Hex, HexNode]:    
        super()._initGameBoard

       



    '''---
    Public
    ---'''
    # Override
    def makeMove(self, player: int, X: Hex) -> None:
        super().makeMove(player, X)

    def getNumPaths(self) -> int:
        """Get the total number of paths that have the best cost"""

        return 0

    def getNumPathsToHex(self, X: Hex) -> int:
        """Get the number of paths to a given hex"""

        return 0

    def getNumPathsFromHex(self, X: Hex) -> int:
        """Get the number of paths from a given Hex"""

        return 0
