from dataclasses import dataclass
from hexBoy.hex.node.HexNode import HexNode, Hex, HexType, DefaultHexType

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

    empty: HexPlayerInfo = HexPlayerInfo(
        player = 0,
        hex = DefaultHexType,
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

    def checkIfBarrier(player: int, X: HexNode, useEmpty=True) -> bool:
        """Check if the hex is a barrier to the player"""
        return not (
            X.getHexType().player == player # player space
            or (useEmpty and X.getHexType() == HexGameRules.empty.hex)# or able to use empty space
        )

    def getPlayerHex(player: int) -> HexType:
        """Get the HexType for the player"""
        if (player == 1): # blue
            return HexGameRules.blue.hex
        elif (player == 2): # red
            return HexGameRules.red.hex
        else: # empty
            return HexGameRules.empty.hex 
