from hexBoy.models.SortedDict import SortedDict

def GetStrongMoves(board, player):
    """Get all of the hexes that"""

    playerMoves = board.getPlayerMoves(player)
    allAdjHexes = SortedDict()
    satelliteHexes = SortedDict()

    strongMoves = []

    # Get adjacent hexes 
    for move in playerMoves: 
        adjHexes = board.getAdjacentSpaces(move)
        for ax in adjHexes:
            if (ax not in playerMoves and board.validateMove(ax)):
                allAdjHexes[ax] = ax

    # go through adjacent hexes 
    for ax in allAdjHexes:
        satHexes = board.getAdjacentSpaces(ax)
        for sx in satHexes:
            # Check that move isn't a taken hex or other adjacent move
            if ((board.validateMove(sx)) and not allAdjHexes.hasKey(sx)):
                # hex is a potential strong move. start counting 
                if (satelliteHexes.hasKey(sx)):
                    satelliteHexes[sx] += 1
                else:
                    satelliteHexes[sx] = 1

    while (len(satelliteHexes) != 0):
        x = satelliteHexes.popItem()
        if (x[1] >= 2):
            strongMoves.append(x[0])

    return strongMoves
