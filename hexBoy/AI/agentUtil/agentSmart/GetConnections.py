from typing import List, Tuple
from hexBoy.models.SortedDict import SortedDict
from hexBoy.hex.HexBoard import Board

def GetConnections(board: Board, playerId: int) -> Tuple[List[int], List[int]]:
    """Get the tuple of (weak, strong) connections for a player"""

    #TODO create type for hex coord instead of Tuple(int,int)

    weakConnections: List[Tuple(int,int)] = []
    strongConnections: List[Tuple(int,int)] = []
    playerMoves: List[Tuple(int,int)] = board.getPlayerMoves(playerId)
    playerEndZone: List[Tuple(int,int)] = board.getPlayerEndZone(playerId)
    clusterId: int = 0
    clusters: SortedDict = SortedDict() # int -> tuple
    hexToCluster: SortedDict = SortedDict() # tuple -> int

    # Sort By lowest length 
    def sortFunc(item): return len(item[1])
    connectionHexes = SortedDict(getSortValue = sortFunc)

    # Group connected hexes into clusters (include player end zone)
    visitedHexes: List[Tuple(int,int)] = []
    allPlayerMoves = [*playerMoves, *playerEndZone]
    for pm in allPlayerMoves:
        if (pm in visitedHexes): 
            continue

        visitedHexes.append(pm)
        clusters[clusterId] = [pm]
        hexToCluster[pm] = clusterId

        lookThroughHexes = SortedDict()
        lookThroughHexes[pm] = 0
        while (len(lookThroughHexes) > 0):
            X = lookThroughHexes.popItem()[0]

            adjacentHexes = board.getAdjacentSpaces(X)
            for aX in adjacentHexes:
                if (
                    (aX in allPlayerMoves)
                    and aX not in visitedHexes
                ):
                    # add hex to cluster
                    clusters[clusterId].append(aX)
                    hexToCluster[aX] = clusterId
                    visitedHexes.append(aX)
                    lookThroughHexes[aX] = 0

        clusterId += 1

    # Get adjacent Hexes per cluster and store what clusters they connect in a dict
    for C in clusters.getKeys():
        clusterAdjacentHexes = []
        # Go through each move in the cluster and get all valid adjacent hexes
        for pm in clusters[C]: 
            adjXs = board.getAdjacentSpaces(pm)
            for aX in adjXs:
                if (aX not in clusterAdjacentHexes and board.validateMove(aX)):
                    clusterAdjacentHexes.append(aX)

        # Go through adjacent hexes and get possible connections to other clusters
        for aX in clusterAdjacentHexes:
            if (aX in connectionHexes): 
                continue

            connectedClusters = []
            satHexes = board.getAdjacentSpaces(aX)
            for sX in satHexes:
                if (sX in allPlayerMoves):
                    connectedClusters.append(hexToCluster[sX])

            # len 1 means no connections
            if (len(set(connectedClusters)) > 1):
                connectionHexes[aX] = list(set(connectedClusters))

    # Go through the connections
    for cX in connectionHexes.getKeys():
        isStrongConnection = False

        for X in connectionHexes:
            # Compare the connected clusters between hexes. If they connect the same ones then they are strong. 
            if (
                (
                    X != cX 
                    and (set(connectionHexes[cX]).issubset(set(connectionHexes[X])))
                )
                or len(connectionHexes[cX]) == 3 # All connections with 3 clusters are strong
            ):
                isStrongConnection = True
                continue

        if (isStrongConnection):
            strongConnections.append(cX)
        else:
            weakConnections.append(cX)

    return (weakConnections, strongConnections)
