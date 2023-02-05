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

    def _getAvailableAdjacentHexes(self, X: HexNode) -> List[HexNode]:
        """Get ADjacent spaces of a node. Include cluster adjacent hexes"""
        nodes: SortedDict = self._board.getNodeDict()
        adjSpaces: List[Hex]
        adjHexes: List[HexNode]
        if (X.getHexType().xType == 2): # TODO prods set to hexrules.edge
            return [] # COMEBACK this might need to return dads/sons

        elif (X.getHexType().player == self._playerInfo.player):
            # player move, use cluster's adjacent hexes as nodes adjHexes
            adjSpaces = self._getClusterAdjacentSpaces(self._hexToCluster[X])

        else:
            # regular hex
            adjSpaces = self._board.getAdjacentSpaces(X)

        # convert Hex -> HexNode
        adjHexes = list(map(lambda X: nodes[X], adjSpaces)) 
        adjHexes = list(filter(lambda X: not self._checkIfBarrier(X), adjHexes))

        return adjHexes

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

        print() # XXX
        print(player, move) # XXX
        print() # XXX

        nodes: Dict[Hex, HexNode] = self._board.getNodeDict()
        X: HexNode = nodes[move]
        deadCells: SortedDict = SortedDict() # Nodes to ignore when updating parents

        # Store Dads and Sons, If a node's path/dist increases update sons/dads
        sonDependencies: SortedDict = SortedDict()
        dadDependencies: SortedDict = SortedDict()

        sonUpdate: SortedDict = SortedDict()
        dadUpdate: SortedDict = SortedDict()

        def _sortFuncByDepth(item: Tuple[HexNode, int]) -> int:
            return item[1]

        def _updateNode(X: HexNode) -> None:
            """Update PCD, Set Best dads/sons for the node"""

            if (X.getHexType().xType == 2): 
                return [] # Edge

            # print('    ', X) # XXX


            originalP: int = X.getPath()
            originalD: int = X.getDist()

            # TODO maybe make this adjacent spaces -> Hexes with barrier check into function. Its used later
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
            adjHexes = list(filter(lambda X: not self._checkIfBarrier(X), adjHexes))

            print(X, ' \t', X.getBest(), X.getPath(), X.getDist(), adjHexes, X.getDads(), X.getSons()) # XXX

            # Get best dads and sons costs
            bestDadPC: int = -1
            bestSonCD: int = -1
            for aX in adjHexes:
                if (not deadCells.hasKey(aX)):
                    if (aX.getPC() < bestDadPC or bestDadPC == -1):
                        bestDadPC = aX.getPC()
                
                    if (aX.getCD() < bestSonCD or bestSonCD == -1):
                        bestSonCD = aX.getCD()

            # Set dads and sons
            bestDads: List[HexNode] = []
            bestSons: List[HexNode] = []
            for aX in adjHexes:
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

            X.setDads(nextDads)
            X.setSons(nextSons)

            X.setPath(X.getDad().getPC())
            X.setDist(X.getSon().getCD())

            print('\t\t', X.getBest(), X.getPath(), X.getDist(), adjHexes, X.getDads(), X.getSons()) # XXX

            # Set the dependencies of this node. If the cost of these nodes increases then this node needs to update again
            for dX in nextDads:
                if dadDependencies.hasKey(dX):
                    dadDependencies[dX] = list(set([*dadDependencies[dX], X]))
                else:
                    dadDependencies[dX] = [X]

            for sX in nextSons:
                if sonDependencies.hasKey(sX):
                    sonDependencies[sX] = list(set([*sonDependencies[sX], X]))
                else:
                    sonDependencies[sX] = [X]


            # Return list of additional nodes that need to be updated
            nodesToUpdate = []
            # Perform updates if the path/dist increased. 
            if (X.getPath() > originalP and dadDependencies.hasKey(X)):
                for dX in dadDependencies[X]:
                    nodesToUpdate.append(dX)

            if (X.getDist() > originalD and sonDependencies.hasKey(X)):
                for sX in sonDependencies[X]:
                    nodesToUpdate.append(sX)

            return nodesToUpdate

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

        # Handle player move
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

        # Handle opp move
        # else:
        #     # opp move; Go through adjacent nodes and remove this node from their families
        #     for a in self._board.getAdjacentSpaces(X):
        #         aX = nodes[a]
        #         if (not self._checkIfBarrier(aX)):
        #             aX.delDad(X)
        #             aX.delSon(X)

        # Update family
        currentNode: HexNode
        order: int
        depth: int

        # Path find; update family and get path update order
        openNodes = SortedDict(getSortValue=_sortFuncByDepth)
        closedNodes = SortedDict()
        pathOrder = SortedDict(getSortValue=_sortFuncByDepth) # update order for paths to/from
        
        # Starting nodes depend on which player made the move
        # TODO probs change to all adjacent hexes
        if (player == self._playerInfo.player):
            openNodes[X] = 0 # Breadth first from player move
            pathOrder[X] = 0

            for adj in self._board.getAdjacentSpaces(X):
                adjX = nodes[adj]
                if adjX.getHexType().player == 0:
                    openNodes[adjX] = 1
                    # pathOrder[adjX] = 1 # TODO needs to be negative for sons

        else: 
            # Start search with the sons/dads of the taken move
            for adj in self._board.getAdjacentSpaces(X):
                adjX = nodes[adj]
                if not self._checkIfBarrier(adjX):
                    openNodes[adjX] = 0
                    pathOrder[adjX] = 0
                    # print('good', adjX, pathOrder[adjX])

            # for s in X.getSons():
            #     openNodes[s] = 0  
            #     pathOrder[s] = 0

            # for d in X.getDads():
            #     openNodes[d] = 0  
            #     pathOrder[d] = 0

        while (len(openNodes) != 0):
            currentNode, depth = openNodes.popItem()
            closedNodes[currentNode] = None
            currentNode = nodes[currentNode]

            previousCost: int = currentNode.getBest()
            previousDads: List[Hex] = currentNode.getDads()
            previousSons: List[Hex] = currentNode.getSons()

            nodesToUpdate = _updateNode(currentNode) # Family is set

            updatedCost: int = currentNode.getBest()
            updatedDads: List[Hex] = currentNode.getDads()
            updatedSons: List[Hex] = currentNode.getSons()

            didCostChange: bool = previousCost != updatedCost
            didDadsChange: bool = set(previousDads) != set(updatedDads)
            didSonsChange: bool = set(previousSons) != set(updatedSons)

            # Add nodes that need to be updated at the front of the open nodes
            for X in nodesToUpdate:
                openNodes[X] = 0

            # Set pathOrder based on adjacent hex path orders
            # - sons will have a positive value and dads have a negative value
            # - nodes that are player hexes have a 0.5 depth difference so they go before empty hexes
            if not pathOrder.hasKey(currentNode) and currentNode.getHexType().xType == 1:
                # TODO ignore edges

                minPathOrder: int = -1
                fromDadOrSon: bool = None

                uhhDad = None # XXX
                uhhSon = None # XXX

                for dX in updatedDads:
                    if pathOrder.hasKey(dX):
                        if abs(pathOrder[dX]) < minPathOrder or minPathOrder == -1:
                            minPathOrder = abs(pathOrder[dX])
                            fromDadOrSon = True

                            uhhDad = dX # XXX

                for sX in updatedSons:
                    if pathOrder.hasKey(sX):
                        if abs(pathOrder[sX]) < minPathOrder or minPathOrder == -1:
                            minPathOrder = abs(pathOrder[sX])
                            fromDadOrSon = False

                            uhhSon = sX # XXX

                if minPathOrder != -1: # Should always be true
                    minPathOrder = math.floor(minPathOrder)
                    if currentNode.getHexType().player == self._playerInfo.player: # Player hex
                        minPathOrder += 0.5
                    else:
                        minPathOrder += 1

                    # Todo don't like not having an else
                    if (fromDadOrSon): # TODO might be None but probs not, put in a check. 
                        pathOrder[currentNode] = minPathOrder 
                    else:
                        pathOrder[currentNode] = minPathOrder * -1
                    # print('\t\tgood', currentNode, pathOrder[currentNode]) # XXX
                else:  
                    # print('\t\tbad ', currentNode, updatedDads, updatedSons) # XXX
                    pass

                print('\t\t', fromDadOrSon, uhhDad, uhhSon)

            # [x] always add existing hex cluster
            # [x] if cost changed, add all adjacent
            # [x] if sons changed, add dads, append to son update dict
            # [x] if dads changed, add sons, append to dad update dict
            # [x] if dad in dad update dict, add sons, append to dad update dict
            # [x] if son in son update dict, add dads, append to son update dict

            # Add existing hex cluster nodes to open
            cluster: List[HexNode] = []
            if (self._hexToCluster.hasKey(currentNode)):
                cluster = self._clusters[self._hexToCluster[currentNode]]
            for cX in cluster:
                if (not openNodes.hasKey(cX) and not closedNodes.hasKey(cX)):
                    openNodes[cX] = depth

            hexesToAdd: List[Hex] = []
            adjHexes: List[HexNode]

            if didCostChange: 
                # TODO probs skip rest of the checks in this section. this adds all adjacent anyways
                # TODO refactor this section when function is created
                # TODO might need to also add these to dad/son update dict
                adjSpaces: List[Hex] = self._board.getAdjacentSpaces(currentNode)
                adjHexes = list(map(lambda X: nodes[X], adjSpaces)) 
                adjHexes = list(filter(lambda X: not self._checkIfBarrier(X), adjHexes))

                hexesToAdd = adjHexes
                
                # print('\t\tcostChange') # XXX

            # Dads changed so need to update sons
            if didDadsChange:
                if (not dadUpdate.hasKey(currentNode)):
                    dadUpdate[currentNode] = None


                hexesToAdd = [*hexesToAdd, *updatedSons]
                # print('\t\tsons1') # XXX

            # Sons changed need to update dads
            if didSonsChange:
                if (not sonUpdate.hasKey(currentNode)):
                    sonUpdate[currentNode] = None

                hexesToAdd = [*hexesToAdd, *updatedDads]
                # print('\t\tdads1') # XXX
            
            # check dads to see if this node needs to update sons or there is a new dad
            dadUpdate1: bool = True
            dadUpdate2: bool = True
            for dX in updatedDads:
                if dadUpdate.hasKey(dX) and dadUpdate1:
                    dadUpdate1 = False
                    dadUpdate[currentNode] = None
                    hexesToAdd = [*hexesToAdd, *updatedSons]
                    # print('\t\tsons2') # XXX

                    # Check adjacent nodes and see if current node is their dad
                    adjHexes = self._getAvailableAdjacentHexes(currentNode)
                    for adjX in adjHexes:
                        if currentNode in adjX.getDads():
                            hexesToAdd.append(adjX)


                if dX not in previousDads and dadUpdate2:
                    dadUpdate2 = False
                    dadUpdate[currentNode] = None
                    hexesToAdd = [*hexesToAdd, *updatedSons]
                    # print('\t\tsons3') # XXX


            # Check sons to see if this node needs to update dads or there is a new son
            sonUpdate1: bool = True
            sonUpdate2: bool = True
            for sX in updatedSons:
                if sonUpdate.hasKey(sX) and sonUpdate1:
                    sonUpdate1 = False
                    sonUpdate[currentNode] = None
                    hexesToAdd = [*hexesToAdd, *updatedDads]
                    # print('\t\tdads2') # XXX


                    # Check adjacent nodes and see if current node is their son
                    adjHexes = self._getAvailableAdjacentHexes(currentNode)
                    for adjX in adjHexes:
                        if currentNode in adjX.getSons():
                            hexesToAdd.append(adjX)

                if sX not in previousSons and sonUpdate2:
                    sonUpdate2 = False
                    hexesToAdd = [*hexesToAdd, *updatedDads]
                    sonUpdate[currentNode] = None
                    # print('\t\tdads3') # XXX

            # Add hexes to the dict
            hexesToAdd = list(set(hexesToAdd))
            for X in hexesToAdd:
                if (not openNodes.hasKey(X) and not closedNodes.hasKey(X)):
                    openNodes[X] = depth + 1

            print('\t\t', hexesToAdd) # XXX

        # Path find; update paths to
        openNodes = SortedDict(initDict=pathOrder, getSortValue=_sortFuncByDepth)
        closedNodes = SortedDict()
        while (len(openNodes) != 0):
            currentNode, depth = openNodes.popItem()
            closedNodes[currentNode] = None
            currentNode = nodes[currentNode]

            _updateNodePathsTo(currentNode)

            print(depth, '\t', currentNode, '\t', currentNode.getPathsToNode()) # XXX

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

            if (currentNode.getDad() != None 
                and currentNode.getDad().getBest() < bestBest 
                or bestBest == -1
            ):
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
        print() # XXX
        dad: HexNode
        for X in closedNodes.getKeys():
            dad = X.getDad()
            if (dad != None): # XXX
                print(dad, dad.getBest(), dad.getPathsToNode()) # XXX
            if (dad != None and dad.getBest() == bestBest):
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
