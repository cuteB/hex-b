import math
from typing import Callable, Dict, List, Tuple

from hexBoy.hex.board.HexBoard import Board
from hexBoy.hex.game.HexGameRules import HexGameRules, HexPlayerInfo
from hexBoy.hex.node.HexNode import Hex, HexNode
from hexBoy.models.SortedDict import SortedDict

class NumPathFinder:
    """Track the number of best paths a player has on the board. Need to initialize board and then update each move"""

    _board: Board
    _checkIfBarrier: Callable[[HexNode], bool]    
    _heuristicFunc: Callable[[HexNode, HexNode], int]  # Heuristic function for A*

    _playerInfo: HexPlayerInfo

    _clusterId: int = 0
    _clusters: SortedDict # int -> List[Hex]    
    _hexToCluster: SortedDict # Hex -> int

    def __init__(
        self,
        board: Board,
        player: int
    ):
        """Initialize num path finder
        @param board: Board "The board to observe"
        @param player: int "The player to monitor, sets heuristic and barrier check from player"
        """

        self._board = board
        self._checkIfBarrier=HexGameRules.getCheckIfBarrierFunc(player)
        self._heuristicFunc=HexGameRules.getHeuristicFunc(player)

        self._clusters = SortedDict()
        self._hexToCluster = SortedDict() 
        self._playerInfo = HexGameRules.getPlayerInfo(player)

    def _getClusterAdjacentSpaces(self, cId: int) -> List[Hex]:
        """Get the adjacent spaces around a cluster"""
        clusterHexes = self._clusters[cId]
        adjHexesToCluster = []

        for cX in clusterHexes:
            adjHexes = self._board.getAdjacentSpaces(cX)
            for aX in adjHexes:
                if (aX not in clusterHexes and aX not in adjHexesToCluster):
                    adjHexesToCluster.append(aX)

        return adjHexesToCluster

    def initEmptyBoard(self) -> None:
        """Initialize an empty Hex Board for the player. Set dads/sons and the paths to/from for each node."""

        # Init all the nodes with their costs and family
        nodes: Dict[Hex, HexNode] = self._board.getNodeDict()

        def _sortFuncByHeur(item: Tuple[HexNode, HexNode]) -> int:
            """sort by heur. go row by row """
            return self._heuristicFunc(item[1], None)

        def _scoreNode(X: HexNode) -> None:
            """Score PCD, set initial family and paths to node"""

            h = self._heuristicFunc(X, None)
            X.setPath(max(11 - h, 0)) # end zones return -1 with heur
            X.setDist(max(h - 1, 0))
            X.setHeur(h - 1)

            if (X.getHexType().xType == 1):
                # Playable board, Set dads/sons 
                for aX in self._board.getAdjacentSpaces(X):
                    adjX = nodes[aX]
                    # Playable Board
                    if (adjX.getHexType().xType == 1): 
                        if (self._heuristicFunc(adjX, None) < self._heuristicFunc(X, None)):
                            X.addSon(adjX)

                        elif (self._heuristicFunc(adjX, None) > self._heuristicFunc(X, None)):
                            X.addDad(adjX)
                    
                    # Player Edge
                    elif (adjX.getHexType().player == self._playerInfo.player 
                        and(X[0] == adjX[0] or X[1] == adjX[1])
                    ): # Player edge Hex in same row or col
                        if (self._heuristicFunc(adjX, None) < self._heuristicFunc(X, None)):
                            X.setSon(adjX) # only have one son to the edge
                            adjX.setDad(X)

                        elif (self._heuristicFunc(adjX, None) > self._heuristicFunc(X, None)):
                            X.setDad(adjX) # only have one dad from the edge
                            adjX.setSon(X)

            # Set paths to
            if (len(X.getDads()) == 0):
                # Edges with no dads have 1 path
                X.setPathsToNode(1)

            else:
                # Regular node
                X.updatePathsToNodeWithDads()

        def _setPathsFrom(X: HexNode) -> None:
            """Set paths from the node"""
            if (len(X.getSons()) == 0):
                # Edges with no sons have 1 path
                X.setPathsFromNode(1)

            else:
                X.updatePathsFromNodeWithSons()

        currentNode: HexNode
        nextNode: HexNode

        # Path find; from start
        openNodes = SortedDict(getSortValue=_sortFuncByHeur, reverse=True)
        closedNodes = SortedDict()
        openNodes[self._playerInfo.start] = nodes[self._playerInfo.start]
        while (len(openNodes) != 0):
            currentNode = openNodes.pop()
            closedNodes[currentNode] = None

            _scoreNode(currentNode)
            
            # Add nodes to open
            for nextPos in self._board.getAdjacentSpaces(currentNode):
                nextNode = nodes[nextPos]

                if (not self._checkIfBarrier(nextNode) 
                    and not closedNodes.hasKey(nextPos) 
                    and not openNodes.hasKey(nextPos)
                ):
                    openNodes[nextNode] = nextNode

        # Path find; going backwards
        openNodes = SortedDict(getSortValue=_sortFuncByHeur)
        closedNodes = SortedDict()
        openNodes[self._playerInfo.end] = nodes[self._playerInfo.end]
        while (len(openNodes) != 0):
            currentNode = openNodes.pop()
            closedNodes[currentNode] = None

            _setPathsFrom(currentNode)

            # Add nodes to open
            for nextPos in self._board.getAdjacentSpaces(currentNode):
                nextNode = nodes[nextPos]

                if (not self._checkIfBarrier(nextNode) 
                    and not closedNodes.hasKey(nextPos) 
                    and not openNodes.hasKey(nextPos)
                ):
                    openNodes[nextNode] = nextNode

    def updateMove(self, player: int, move: Hex) -> None:
        """Update board with the new move. Set Dads, Sons, and num paths to/from"""

        # print() # XXX
        # print(player, move) # XXX
        # print() # XXX

        nodes: Dict[Hex, HexNode] = self._board.getNodeDict()
        X: HexNode = nodes[move]
        deadCells: SortedDict = SortedDict() # Nodes to ignore when updating parents

        # Store Dads and Sons, If a node's path/dist increases update sons/dads
        sonDependencies: SortedDict = SortedDict()
        dadDependencies: SortedDict = SortedDict()

        def _sortFuncByDepth(item: Tuple[HexNode, int]) -> int:
            return item[1]

        def _updateNode(X: HexNode) -> None:
            """Update PCD, Set Best dads/sons for the node"""

            if (X.getHexType().xType == 2): 
                return # Edge

            originalP: int = X.getPath()
            originalD: int = X.getDist()

            # get Adjacent Hexes            
            adjSpaces: List[Hex]
            adjHexes: List[HexNode]
            if (X.getHexType().player == self._playerInfo.player):
                # player move, use cluster's adjacent hexes as nodes adjHexes
                adjSpaces = self._getClusterAdjacentSpaces(self._hexToCluster[X])
            else:
                # regular hex
                adjSpaces = self._board.getAdjacentSpaces(X)
            # convert Hex -> HexNode
            adjHexes = list(map(lambda X: nodes[X], adjSpaces)) 

            # Get best dads and sons costs
            bestDadPC: int = -1
            bestSonCD: int = -1
            for aX in adjHexes:
                if (not self._checkIfBarrier(aX) and not deadCells.hasKey(aX)):
                    if (aX.getPC() < bestDadPC or bestDadPC == -1):
                        bestDadPC = aX.getPC()
                
                    if (aX.getCD() < bestSonCD or bestSonCD == -1):
                        bestSonCD = aX.getCD()

            # Set dads and sons
            bestDads: List[HexNode] = []
            bestSons: List[HexNode] = []
            for aX in adjHexes:
                if (not self._checkIfBarrier(aX)):
                    if (aX.getPC() == bestDadPC):
                        bestDads.append(aX)

                    if (aX.getCD() == bestSonCD):
                        bestSons.append(aX)

            # filter out dads from the same cluster
            dadClusters: List[int] = []
            nextDads: List[HexNode] = []
            for d in bestDads:
                if (d.getHexType().xType == 2):
                    # If best dad is the end zone, set its dads to one of the edges
                    nextDads = [d]
                    break

                elif self._hexToCluster.hasKey(d):
                    # Only add one dad from the same cluster
                    cId: int = self._hexToCluster[d]
                    if cId not in dadClusters:
                        dadClusters.append(cId)
                        nextDads.append(d)
                
                else:
                    nextDads.append(d)

            # filter out sons from the same cluster
            sonClusters: List[int] = []
            nextSons: List[HexNode] = []
            for s in bestSons:
                if s.getHexType().xType == 2:
                    # If best son is the end zone, set its sons to one of the edges
                    nextSons = [s]
                    break

                elif self._hexToCluster.hasKey(s):
                    # Only add one son from the same cluster
                    cId: int = self._hexToCluster[s]
                    if cId not in sonClusters:
                        sonClusters.append(cId)
                        nextSons.append(s)
                
                else:
                    nextSons.append(s)

            # Sons can't be their own grandpa
            if (set(nextDads) == set(nextSons)):
                # 1. identify node as a dead end
                deadCells[X] = None
                # 2. All node updates from now on can't use nodes that are dead ends

            # print(X, X.getBest(), nextDads, nextSons) # XXX

            X.setDads(nextDads)
            X.setSons(nextSons)

            X.setPath(X.getDad().getPC())
            X.setDist(X.getSon().getCD())

            # Set the dependencies of this node. If the cost of these nodes increases then this node needs to update again
            for dX in nextDads:
                if dadDependencies.hasKey(dX):
                    dadDependencies[dX] = [*dadDependencies[dX], X] 
                else:
                    dadDependencies[dX] = [X]

            for sX in nextSons:
                if sonDependencies.hasKey(sX):
                    sonDependencies[sX] = [*sonDependencies[sX], X]
                else:
                    sonDependencies[sX] = [X]

            # Perform updates if the path/dist increased. 
            if (X.getPath() > originalP and dadDependencies.hasKey(X)):
                for dX in dadDependencies[X]:
                    _updateNode(dX)

            if (X.getDist() > originalD and sonDependencies.hasKey(X)):
                for sX in sonDependencies[X]:
                    _updateNode(sX)

        def _updateNodePathsTo(X: HexNode) -> None:
            """Update node's dads, path, and paths to node"""

            if (X.getHexType().xType == 2): # Edge
                return

            X.updatePathsToNodeWithDads()

        def _updateNodePathsFrom(X: HexNode) -> None:
            """Update node's sons, dist and paths from node"""

            if (X.getHexType().xType == 2): # Edge
                return

            X.updatePathsFromNodeWithSons()

        # Handle player/opp move
        if (player == self._playerInfo.player):
            # player move
            adjClusters: List[int] = []
            for aX in self._board.getAdjacentSpaces(move):
                if self._hexToCluster.hasKey(aX):
                    # adjacent Hex is already a player move
                    adjClusters.append(self._hexToCluster[aX])

            adjClusters = list(set(adjClusters)) # Remove duplicates

            if (len(adjClusters) == 0):
                # No adjacent clusters
                self._clusters[self._clusterId] = [move]
                self._hexToCluster[move] = self._clusterId
                self._clusterId += 1

            elif (len(adjClusters) == 1):
                # one adjacent cluster. join that group
                self._clusters[adjClusters[0]].append(move)
                self._hexToCluster[move] = adjClusters[0]

            else:
                # multiple adjacent clusters. join the groups into one and delete the other ids
                adjClusters.sort()
                id = adjClusters[0] 

                Xs = self._clusters[id]
                for i in adjClusters:
                    if i != id:
                        clusterHexes = self._clusters[i] 
                        Xs = [*Xs, *clusterHexes] # TODO maybe concat, idk what its called 
                        for cX in clusterHexes:
                            self._hexToCluster[cX] = id
                        del(self._clusters[i])

                self._clusters[id] = Xs

        else:
            # opp move; Go through adjacent nodes and remove this node from their families
            for a in self._board.getAdjacentSpaces(X):
                aX = nodes[a]
                if (not self._checkIfBarrier(aX)):
                    aX.delDad(X)
                    aX.delSon(X)

        # Update family
        currentNode: HexNode
        order: int
        depth: int

        # Path find; update family and get path update order
        openNodes = SortedDict(getSortValue=_sortFuncByDepth)
        closedNodes = SortedDict()
        pathOrder = SortedDict(getSortValue=_sortFuncByDepth) # update order for paths to/from

        # Starting nodes depend on which player made the move
        if (player == self._playerInfo.player):
            openNodes[X] = 0 # Breadth first from player move
            pathOrder[X] = 0
        else: 
            # Start search with the sons/dads of the taken move
            for s in X.getSons():
                openNodes[s] = 0  
                pathOrder[s] = 0

            for d in X.getDads():
                openNodes[d] = 0  
                pathOrder[d] = 0

        while (len(openNodes) != 0):
            currentNode, depth = openNodes.popItem()
            closedNodes[currentNode] = None
            order = pathOrder[currentNode]
            currentNode = nodes[currentNode]

            _updateNode(currentNode) # Family is set

            cluster: List[HexNode] = []
            if (self._hexToCluster.hasKey(currentNode)):
                cluster = self._clusters[self._hexToCluster[currentNode]]

            # Add existing hex cluster nodes to open
            for cX in cluster:
                if (not openNodes.hasKey(cX) and not closedNodes.hasKey(cX)):
                    openNodes[cX] = depth
                    pathOrder[cX] = order

            # Add sons to open
            # - nodes that are player hexes have a 0.5 depth difference so they go before empty hexes
            sons: List[HexNode] = currentNode.getSons()
            for sX in sons:
                if (not openNodes.hasKey(sX) and not closedNodes.hasKey(sX)):
                    openNodes[sX] = depth + 1
                    
                    if sX.getHexType().player == self._playerInfo.player: # Player hex
                        pathOrder[sX] = math.floor(order) + 0.5
                    
                    else: 
                        pathOrder[sX] = math.floor(order) + 1 

            # Add dads to open
            # - nodes that are player hexes have a 0.5 depth difference so they go before empty hexes
            dads: List[HexNode] = currentNode.getDads()
            for dX in dads:
                if (not openNodes.hasKey(dX) and not closedNodes.hasKey(dX)):
                    openNodes[dX] = depth + 1

                    if dX.getHexType().player == self._playerInfo.player: # Player hex
                        pathOrder[dX] = math.floor(order) - 0.5
                    
                    else: 
                        pathOrder[dX] = math.floor(order) - 1

        # Path find; update paths to
        openNodes = SortedDict(initDict=pathOrder, getSortValue=_sortFuncByDepth)
        closedNodes = SortedDict()
        while (len(openNodes) != 0):
            currentNode = openNodes.popKey()
            closedNodes[currentNode] = None
            currentNode = nodes[currentNode]

            _updateNodePathsTo(currentNode)

        # Path find; update paths From
        openNodes = SortedDict(initDict=pathOrder, getSortValue=_sortFuncByDepth, reverse=True)
        closedNodes = SortedDict()
        while (len(openNodes) != 0):
            currentNode = openNodes.popKey()
            closedNodes[currentNode] = None
            currentNode = nodes[currentNode]

            _updateNodePathsFrom(currentNode)

    def getNumPaths(self) -> int:
        """Get the total number of paths that have the best cost"""

        numPaths: int = 0
        bestBest: int = -1 # best PCD of a node

        nodes: Dict[Hex, HexNode] = self._board.getNodeDict()
        currentNode: HexNode
        nextNode: HexNode

        # Path find player end edges
        openNodes: SortedDict = SortedDict()
        closedNodes: SortedDict = SortedDict()
        openNodes[self._playerInfo.end] = nodes[self._playerInfo.end]
        while (len(openNodes) != 0):
            currentNode = openNodes.pop()
            closedNodes[currentNode] = None

            if (currentNode.getDad().getBest() < bestBest or bestBest == -1):
                bestBest = currentNode.getDad().getBest()

            for nextPos in self._board.getAdjacentSpaces(currentNode):
                nextNode = nodes[nextPos]

                # Add player edges
                if (not self._checkIfBarrier(nextNode) 
                    and not closedNodes.hasKey(nextPos) 
                    and not openNodes.hasKey(nextPos)
                    and nextNode.getHexType().xType == 2
                ):
                    openNodes[nextNode] = nextNode

        # Count up paths for the edges with the best cost
        # print()
        dad: HexNode
        for X in closedNodes.getKeys():
            dad = X.getDad()
            # print(dad, dad.getBest(), dad.getPathsToNode()) # XXX
            if (dad.getBest() == bestBest):
                numPaths += dad.getPathsToNode()

        # print(numPaths) # XXX
        return numPaths

    def getNumPathsToHex(self, X: Hex) -> int:
        """Get the number of paths to a given hex. Returns the current value and doesn't do any updates"""

        node: HexNode = self._board.getNodeDict()[X]
        return node.getPathsToNode()

    def getNumPathsFromHex(self, X: Hex) -> int:
        """Get the number of paths from a given Hex. Returns the current value and doesn't do any updates"""

        node: HexNode = self._board.getNodeDict()[X]
        return node.getPathsFromNode()
