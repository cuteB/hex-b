from typing import List

from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.node.HexNode import Hex
from hexBoy.models.SortedDict import SortedDict

def GetStrongMoves(player: int, board: HexBoard) -> List[Hex]:
    """Get all of the hexes that are considered strong moves"""

    strongMoves: List[Hex] = []
    playerMoves: List[Hex] = board.getPlayerMoves(player)
    adjHexes: List[Hex] = None
    satHexes: List[Hex] = None
    allAdjHexes: SortedDict  = SortedDict()
    satelliteHexes: SortedDict = SortedDict()
    strongHexes: SortedDict = SortedDict()

    # Get all adjacent hexes for the player, Strong moves can't be in this set
    for move in playerMoves: 
        adjHexes = board.getAdjacentSpaces(move)
        for ax in adjHexes:
            if (board.validateMove(ax)):
                allAdjHexes[ax] = ax

    # go through each move and find the strong moves from that hex
    for move in playerMoves: 
        adjHexes = board.getAdjacentSpaces(move)
        for ax in adjHexes:
            if (board.validateMove(ax)):
                satHexes = board.getAdjacentSpaces(ax)
                for sx in satHexes:
                    # Check that move isn't a taken hex or other adjacent move
                    if ((board.validateMove(sx)) and not allAdjHexes.hasKey(sx)):
                        # hex is a potential strong move. start counting 
                        if (satelliteHexes.hasKey(sx)):
                            satelliteHexes[sx] += 1
                        else:
                            satelliteHexes[sx] = 1

        # Get strong hexes for this move
        while (len(satelliteHexes) != 0):
            x = satelliteHexes.popItem()
            if (x[1] >= 2):
                strongHexes[x[0]] = x[0]

    # dict to list
    while (len(strongHexes) > 0):
        strongMoves.append(strongHexes.popItem()[0])

    return strongMoves
