from typing import Callable
from dataclasses import dataclass
from hexBoy.hex.node.HexNode import HexNode, Hex, HexType

@dataclass
class HexPlayerInfo:
    """Player info for the game. Includes player id, start/end positions and HexTypes"""

    player: int = None
    start: Hex = None
    end: Hex = None
    hex: HexType = None
    edge: HexType = None

class HexGameRules:
    """Rules of the game. Contains player info and Barrier Check"""

    # xType 1: Playable Board Hex
    # xType 2: Edge Hex

    empty: HexPlayerInfo = HexPlayerInfo(
        player = 0,
        hex = HexType(player=0, xType=1, cost=1)
    )

    blue: HexPlayerInfo = HexPlayerInfo(
        player = 1,
        start = Hex((5,-1)),
        end = Hex((5,11)),
        hex = HexType(player=1, xType=1, cost=0),
        edge = HexType(player=1, xType=2, cost=0)
    )

    red: HexPlayerInfo = HexPlayerInfo(
        player = 2,
        start = Hex((-1,5)),
        end = Hex((11,5)),
        hex = HexType(player=2, xType=1, cost=0),
        edge = HexType(player=2, xType=2, cost=0)
    )

    def getPlayerInfo(player: int) -> HexPlayerInfo:
        """Get the specified player's info"""
        
        if (player == 1): # blue
            return HexGameRules.blue
        if (player == 2): # red
            return HexGameRules.red
        else: # empty (don't really need this one but probably better than None)
            return HexGameRules.empty

    def getOpponentInfo(player: int) -> HexPlayerInfo:
        """Get the opponent's info given the player"""
        
        if (player == 1): # blue, give red
            return HexGameRules.red
        if (player == 2): # red, give blue
            return HexGameRules.blue
        else: # empty (don't really need this one but probably better than None)
            return HexGameRules.empty

    def getCheckIfBarrierFunc(player: int, useEmpty=True) -> Callable[[HexNode], bool]:
        """Check if the hex is a barrier to the player"""

        def checkIfBarrier(X: HexNode):
            return not (
                X.getHexType().player == player # player space
                or (useEmpty and X.getHexType() == HexGameRules.empty.hex)# or able to use empty space
            )

        return checkIfBarrier

    def getPlayerHex(player: int) -> HexType:
        """Get the HexType for the player"""

        if (player == 1): # blue
            return HexGameRules.blue.hex
        elif (player == 2): # red
            return HexGameRules.red.hex
        else: # empty
            return HexGameRules.empty.hex 

    def getHeuristicFunc(player: int) -> Callable[[Hex, Hex], int]:
        """Return the heuristic function for the player used in the pathfinder"""

        if (player == 1): # blue
            i = 1
        else: # red
            i = 0

        def heuristicFunc(X: Hex, _: Hex) -> int:
            """Manhattan distance to end zone"""
            return 11 - X[i]

        return heuristicFunc
