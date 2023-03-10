import math
from typing import Callable, Dict, List, Tuple

from hexBoy.hex.board.HexBoard import Board
from hexBoy.hex.game.HexGameRules import HexGameRules, HexPlayerInfo
from hexBoy.hex.node.HexNode import Hex, HexNode
from hexBoy.models.SortedDict import SortedDict
from hexBoy.pathfinder.PathBoy import PathBoy

class NumPathFinder:
    """Track the number of best paths a player has on the board. Need to initialize board and then update each move"""

    _board: Board
    _checkIfBarrier: Callable[[HexNode], bool]    
    _heuristicFunc: Callable[[HexNode, HexNode], int]  # Heuristic function for A*

    _playerInfo: HexPlayerInfo

    _pf: PathBoy

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

        # [ ] would eventually like to change a move from one player to next but not really relevant to the game
        # [ ] in late game the secondary paths don't seem to be updating.

        print() # XXX
        print("Board", self._playerInfo.player, "player", player, move) # XXX
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
        
        def _sortFuncPathOrder(item: Tuple[HexNode, int]) -> int:
            return item[0].getBest() * 100 + item[1]

        def _updateNodeFamily(X: HexNode) -> None:
            """Update PCD, Set Best dads/sons for the node"""

            if (X.getHexType().xType == 2): 
                return [] # Edge

            # print('    ', X) # XXX


            originalP: int = X.getPath()
            originalD: int = X.getDist()

            # TODO maybe make this adjacent spaces -> Hexes with barrier check into function. Its used later
            # get Adjacent Hexes            
            # adjSpaces: List[Hex]
            # adjHexes: List[HexNode]
            # if (X.getHexType().player == self._playerInfo.player):
            #     # player move, use cluster's adjacent hexes as nodes adjHexes
            #     adjSpaces = self._getClusterAdjacentSpaces(self._hexToCluster[X])
            # else:
            #     # regular hex
            #     adjSpaces = self._board.getAdjacentSpaces(X)
            # # convert Hex -> HexNode
            # adjHexes = list(map(lambda X: nodes[X], adjSpaces)) 
            # adjHexes = list(filter(lambda X: not self._checkIfBarrier(X), adjHexes))

            adjHexes = self._getAvailableAdjacentHexes(X)

            # print(X, ' \t', X.getBest(), X.getPath(), X.getDist(), adjHexes, X.getDads(), X.getSons()) # XXX

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
            if (set(nextDads) == set(nextSons) and X.getHexType().player == self._playerInfo.player):
                # 1. identify node as a dead end
                deadCells[X] = None
                # 2. All node updates from now on can't use nodes that are dead ends

            # [ ] Node can either be a dad or son 
            # if (len(nextDads) < len(nextSons)):
            #     for dX in nextDads:
            #         if dX in nextSons and dX.getHexType().player != self._playerInfo.player:
            #             nextSons.remove(dX)

            # else:
            #     for sX in nextSons:
            #         if sX in nextDads and sX.getHexType().player != self._playerInfo.player:
            #             nextDads.remove(sX)

            X.setDads(nextDads)
            X.setSons(nextSons)

            if(len(nextDads) == 0 or len(nextSons) == 0):
                return []# TODO might add this part to the dead cell part
            


            X.setPath(X.getDad().getPC())
            X.setDist(X.getSon().getCD())

            # print('\t\t', X.getBest(), X.getPath(), X.getDist(), adjHexes, X.getDads(), X.getSons()) # XXX

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

                Xs.append(move)
                self._clusters[id] = Xs
                self._hexToCluster[move] = id

        # Handle opp move
        # else:
        #     # opp move; Go through adjacent nodes and remove this node from their families
        #     for a in self._board.getAdjacentSpaces(X):
        #         aX = nodes[a]
        #         if (not self._checkIfBarrier(aX)):
        #             aX.delDad(X)
        #             aX.delSon(X)

        # check if there is a path available
        # bestPath = self._pf.findPath(self._playerInfo.start, self._playerInfo.end)
        # if (len(bestPath) == 0): 
        #     return 0

        # Update family
        currentNode: HexNode
        order: int
        depth: int

        # Path find; update family and get path update order
        openNodes = SortedDict(getSortValue=_sortFuncByDepth)
        closedNodes = SortedDict()
        pathOrder = SortedDict(getSortValue=_sortFuncPathOrder) # update order for paths to/from
        outOfOrderNodes: SortedDict = SortedDict() 
        costAlreadyUpdated: SortedDict = SortedDict()


        def checkAddNodeToOpenNodes(_X: Hex) -> bool:
            """Return if a node should be added to open nodes"""
            X: HexNode = nodes[_X]
            return (
                not openNodes.hasKey(X) 
                and not closedNodes.hasKey(X)
                and X.getHexType().xType == 1
            )
        
        # Starting nodes depend on which player made the move
        # TODO probs change to all adjacent hexes
        if (player == self._playerInfo.player):
            openNodes[X] = 0 # Breadth first from player move
            # pathOrder[X] = 0

            for adj in self._board.getAdjacentSpaces(X):
                adjX = nodes[adj]
                if adjX.getHexType().player == 0 and checkAddNodeToOpenNodes(adjX):
                    openNodes[adjX] = 1
                    # pathOrder[adjX] = 1 # TODO needs to be negative for sons

        else: 
            # Start search with the sons/dads of the taken move
            for adj in self._board.getAdjacentSpaces(X):
                adjX = nodes[adj]
                if not self._checkIfBarrier(adjX) and checkAddNodeToOpenNodes(adjX):
                    openNodes[adjX] = 0
                    # pathOrder[adjX] = 0
                    # print('good', adjX, pathOrder[adjX])

            # for s in X.getSons():
            #     openNodes[s] = 0  
            #     pathOrder[s] = 0

            # for d in X.getDads():
            #     openNodes[d] = 0  
            #     pathOrder[d] = 0

        while (len(openNodes) != 0):
            currentNode, depth = openNodes.popItem()

            # if the cluster is already closed then open all of the cluster's nodes
            if (self._hexToCluster.hasKey(currentNode) and closedNodes.hasKey(currentNode)):
                clusterId = self._hexToCluster[currentNode]
                cluster = self._clusters[clusterId]
                for cX in cluster:
                    if (closedNodes.hasKey(cX)):
                        del closedNodes[cX]

            closedNodes[currentNode] = depth
            currentNode = nodes[currentNode]

            previousCost: int = currentNode.getBest()
            previousDads: List[Hex] = currentNode.getDads()
            previousSons: List[Hex] = currentNode.getSons()


            # if (not outOfOrderNodes.hasKey(currentNode)):
            #     nodesToUpdate = _updateNodeFamily(currentNode) # Family is set
            # else:
            #     print(currentNode)
            #     nodesToUpdate = []
            nodesToUpdate = _updateNodeFamily(currentNode) # Family is set


            updatedCost: int = currentNode.getBest()
            updatedDads: List[Hex] = currentNode.getDads()
            updatedSons: List[Hex] = currentNode.getSons()

            didCostChange: bool = previousCost != updatedCost
            didDadsChange: bool = set(previousDads) != set(updatedDads)
            didSonsChange: bool = set(previousSons) != set(updatedSons)

            # Add nodes that need to be updated at the front of the open nodes
            for adjX in nodesToUpdate:
                if (checkAddNodeToOpenNodes(adjX)):
                    openNodes[adjX] = 0

            # Set pathOrder based on adjacent hex path orders
            # - sons will have a positive value and dads have a negative value
            # - nodes that are player hexes have a 0.5 depth difference so they go before empty hexes
            
            if (not outOfOrderNodes.hasKey(currentNode)):
                minPathOrder: int = -1
                actualPathOrder: int = -1
                increment: int = 0
                fromDadOrSon: bool = None # true: dad, false: son

                uhhDad = None # XXX
                uhhSon = None # XXX

                # Check Dads
                for dX in updatedDads:
                    if pathOrder.hasKey(dX):
                        if abs(pathOrder[dX]) < minPathOrder or minPathOrder == -1:
                            minPathOrder = abs(pathOrder[dX])
                            actualPathOrder = pathOrder[dX]
                            fromDadOrSon = True

                            uhhDad = dX # XXX

                for sX in updatedSons:
                    if pathOrder.hasKey(sX):
                        if abs(pathOrder[sX]) < minPathOrder or minPathOrder == -1:
                            minPathOrder = abs(pathOrder[sX])
                            actualPathOrder = pathOrder[sX]
                            fromDadOrSon = False

                            uhhSon = sX # XXX

                if minPathOrder != -1: # TODO also check if fromDadOrSon == None
                    if currentNode.getHexType().player == self._playerInfo.player: # Player hex
                        increment = 0.5
                    else:
                        increment = 1

                    # Todo don't like not having an else
                    if (fromDadOrSon): # TODO might be None but probs not, put in a check. 
                        # 
                        actualPathOrder = math.floor(actualPathOrder) 

                        pathOrder[currentNode] = actualPathOrder + increment
                        # print('\t\t\t good', pathOrder[currentNode], "fromDad", uhhDad, "=", actualPathOrder, "+", increment) # XXX

                    else:
                        actualPathOrder = math.ceil(actualPathOrder) 

                        pathOrder[currentNode] = actualPathOrder - increment
                        # print('\t\t\t good', pathOrder[currentNode], "fromSon", uhhSon, "=", actualPathOrder, "-", increment) # XXX
                else: 
                    if currentNode.getHexType().player == self._playerInfo.player: # Player hex
                        pathOrder[currentNode] = 0.5 # This has to be positive
                    else:
                        pathOrder[currentNode] = 0 
                    # print('\t\t\t new ', pathOrder[currentNode]) # XXX

                # print('\t\t\t', fromDadOrSon, uhhDad, uhhSon) # XXX

                # if node is part of a cluster then set the path order of all of the nodes in the cluster
                if (self._hexToCluster.hasKey(currentNode)):
                    clusterId = self._hexToCluster[currentNode]
                    cluster = self._clusters[clusterId]
                    for cX in cluster:
                        pathOrder[nodes[cX]] = pathOrder[currentNode]

            else:
                del outOfOrderNodes[currentNode]

            currentPathOrder = pathOrder[currentNode]
            if abs(currentPathOrder) > 130: break # XXX
            # check if nodes adjacent nodes, that have their path set, are still in order compared to currentNode

            # [ ] Check if dad order is less than current path order and son order is greater than current path order

            adjHexes = self._getAvailableAdjacentHexes(currentNode)
            for aX in adjHexes: 
                if (pathOrder.hasKey(aX)):
                    aXPathOrder = math.floor(pathOrder[aX])
                    # TODO what does this if do

                    # Adjacent order is too far away from current node order
                    if (
                        (aX in updatedDads and aXPathOrder > currentPathOrder)
                        or (aX in updatedSons and aXPathOrder < currentPathOrder)
                    ):
                        outOfOrderNodes[aX] = None
                        openNodes[aX] = -1

                        # Still need to check if it is a player node to modify increment
                        if aX.getHexType().player == self._playerInfo.player: # Player hex
                            increment = 0.5
                        else:
                            increment = 1

                        if (aX in updatedDads or currentNode in aX.getSons()):
                            pathOrder[aX] = math.ceil(currentPathOrder) - increment

                        elif (aX in updatedSons or currentNode in aX.getDads()):
                            pathOrder[aX] = math.floor(currentPathOrder) + increment
                        
                        else:
                            pathOrder[aX] = currentPathOrder

                        # print ("bad",currentPathOrder, aX, aXPathOrder, "->" , pathOrder[aX]) # XXX



                


            # Add existing hex cluster nodes to open
            # TODO maybe add cluster nodes to hexesToAdd instead of adding them to open here
            hexesToAdd: List[Hex] = []
            if (self._hexToCluster.hasKey(currentNode)):
                hexesToAdd.extend(self._clusters[self._hexToCluster[currentNode]])
            

            adjHexes: List[HexNode]
            if didCostChange: 
                # TODO probs skip rest of the checks in this section. this adds all adjacent anyways
                # TODO refactor this section when function is created
                # TODO might need to also add these to dad/son update dict
                adjHexes = self._getAvailableAdjacentHexes(currentNode)
                costAlreadyUpdated[currentNode] = None

                hexesToAdd.extend(adjHexes)
                
                # print('\t\tcostChange') # XXX

            # Dads changed so need to update sons
            if didDadsChange:
                if (not dadUpdate.hasKey(currentNode)):
                    dadUpdate[currentNode] = None
                    if (self._hexToCluster.hasKey(currentNode)): # TODO double check cluster only gets added once
                        for cX in self._clusters[self._hexToCluster[currentNode]]:
                            dadUpdate[cX] = None


                hexesToAdd.extend(updatedSons)
                # print('\t\tsons1') # XXX

            # Sons changed need to update dads
            if didSonsChange:
                if (not sonUpdate.hasKey(currentNode)):
                    sonUpdate[currentNode] = None

                    if (self._hexToCluster.hasKey(currentNode)): # TODO double check cluster only gets added once
                        for cX in self._clusters[self._hexToCluster[currentNode]]: # TODO holy copy and paste this 
                            sonUpdate[cX] = None

                hexesToAdd.extend(updatedDads)
                # print('\t\tdads1') # XXX
            
            # check dads to see if this node needs to update sons or there is a new dad
            dadUpdate1: bool = True
            dadUpdate2: bool = True
            for dX in updatedDads:
                if dadUpdate.hasKey(dX) and dadUpdate1:
                    dadUpdate1 = False
                    dadUpdate[currentNode] = None
                    hexesToAdd.extend(updatedSons)

                    if (self._hexToCluster.hasKey(currentNode)): # TODO double check cluster only gets added once
                        for cX in self._clusters[self._hexToCluster[currentNode]]:
                            dadUpdate[cX] = None

                    # print('\t\tsons2') # XXX

                    # Check adjacent nodes and see if current node is their dad
                    adjHexes = self._getAvailableAdjacentHexes(currentNode)
                    for adjX in adjHexes:
                        if currentNode in adjX.getDads():
                            hexesToAdd.append(adjX)

                if dX not in previousDads and dadUpdate2:
                    dadUpdate2 = False
                    dadUpdate[currentNode] = None
                    hexesToAdd.extend(updatedSons)
                    # print('\t\tsons3') # XXX

                    if (self._hexToCluster.hasKey(currentNode)): # TODO double check cluster only gets added once
                        for cX in self._clusters[self._hexToCluster[currentNode]]:
                            dadUpdate[cX] = None

            # Check sons to see if this node needs to update dads or there is a new son
            sonUpdate1: bool = True
            sonUpdate2: bool = True
            for sX in updatedSons:
                if sonUpdate.hasKey(sX) and sonUpdate1:
                    sonUpdate1 = False
                    sonUpdate[currentNode] = None
                    hexesToAdd.extend(updatedDads)
                    # print('\t\tdads2') # XXX

                    if (self._hexToCluster.hasKey(currentNode)): # TODO double check cluster only gets added once
                        for cX in self._clusters[self._hexToCluster[currentNode]]:
                            sonUpdate[cX] = None


                    # Check adjacent nodes and see if current node is their son
                    adjHexes = self._getAvailableAdjacentHexes(currentNode)
                    for adjX in adjHexes:
                        if currentNode in adjX.getSons():
                            hexesToAdd.append(adjX)

                if sX not in previousSons and sonUpdate2:
                    sonUpdate2 = False
                    hexesToAdd.extend(updatedDads)
                    sonUpdate[currentNode] = None
                    # print('\t\tdads3') # XXX

                    if (self._hexToCluster.hasKey(currentNode)): # TODO double check cluster only gets added once
                        for cX in self._clusters[self._hexToCluster[currentNode]]:
                            sonUpdate[cX] = None

            # Add hexes to the dict
            hexesToAdd = list(set(hexesToAdd))
            added = [] # XXX
            for addX in hexesToAdd:
                if (checkAddNodeToOpenNodes(addX)):
                    added.append(addX)
                    openNodes[addX] = depth + 1

                elif (closedNodes.hasKey(addX) and didCostChange 
                    and (not costAlreadyUpdated.hasKey(addX) or previousCost < updatedCost)
                ):
                    openNodes[addX] = closedNodes[addX]
                    #del closedNodes[addX]

                    added.append(addX)


            # print('\t\t\t', "add", added, " from", hexesToAdd) # XXX

        # Path find; update paths to
        openNodes = SortedDict(initDict=pathOrder, getSortValue=_sortFuncPathOrder)
        closedNodes = SortedDict()
        while (len(openNodes) != 0):
            currentNode, depth = openNodes.popItem()
            closedNodes[currentNode] = None
            currentNode = nodes[currentNode]

            _updateNodePathsTo(currentNode)

            # print(depth, '\t', currentNode, '\t', currentNode.getPathsToNode()) # XXX

        # Path find; update paths From
        # print() # XXX
        openNodes = SortedDict(initDict=pathOrder, getSortValue=_sortFuncPathOrder, reverse=True)
        closedNodes = SortedDict()
        while (len(openNodes) != 0):
            currentNode, depth = openNodes.popItem()
            closedNodes[currentNode] = None
            currentNode = nodes[currentNode]

            _updateNodePathsFrom(currentNode)

            # print(depth, '\t', currentNode, '\t', currentNode.getPathsFromNode()) # XXX


    def getNumPaths(self) -> int:
        """Get the total number of paths that have the best cost"""

        numPaths: int = 0
        bestBest: int = -1 # best PCD of a node

        nodes: Dict[Hex, HexNode] = self._board.getNodeDict()
        currentNode: HexNode
        nextNode: HexNode

        if not self.checkIfPlayerStillHasPath():
            return 0

        # Path find player end edges
        openNodes: SortedDict = SortedDict()
        closedNodes: SortedDict = SortedDict()
        openNodes[self._playerInfo.end] = nodes[self._playerInfo.end]
        while (len(openNodes) != 0):
            currentNode = openNodes.pop()
            closedNodes[currentNode] = None

            if (currentNode.getDad() != None 
                and not self._checkIfBarrier(currentNode.getDad())
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
                pass
                print(dad, dad.getBest(), dad.getPathsToNode(), not self._checkIfBarrier(X.getDad())) # XXX
            if (dad != None and dad.getBest() == bestBest and not self._checkIfBarrier(X.getDad())):
                numPaths += dad.getPathsToNode()

        print(numPaths) # XXX
        return numPaths

    def getNumPathsToHex(self, X: Hex) -> int:
        """Get the number of paths to a given hex. Returns the current value and doesn't do any updates"""

        node: HexNode = self._board.getNodeDict()[X]
        return node.getPathsToNode()

    def getNumPathsFromHex(self, X: Hex) -> int:
        """Get the number of paths from a given Hex. Returns the current value and doesn't do any updates"""

        node: HexNode = self._board.getNodeDict()[X]
        return node.getPathsFromNode()


    def checkIfPlayerStillHasPath(self):
        """Using an existing node dict from the num path finder get the best path"""

        def _sortFunc(item: Tuple[HexNode, int]) -> int:
            return item[0].getDist()
        
        def _tempGetAdjacentSpaces(X: HexNode) -> List[HexNode]:
            nodes: SortedDict = self._board.getNodeDict()
            adjSpaces: List[Hex]
            adjHexes: List[HexNode]
                # regular hex
            adjSpaces = self._board.getAdjacentSpaces(X)

            # convert Hex -> HexNode
            adjHexes = list(map(lambda X: nodes[X], adjSpaces)) 
            adjHexes = list(filter(lambda X: not self._checkIfBarrier(X), adjHexes))

            return adjHexes

        nodes: Dict[Hex, HexNode] = self._board.getNodeDict()

        openNodes: SortedDict = SortedDict(getSortValue=_sortFunc)
        closedNodes: SortedDict = SortedDict()

        currentNode: HexNode  = nodes[self._playerInfo.start] 
        openNodes[currentNode] = currentNode

        # Path find; start on the start, add all of the edges and find any path to the end
        while currentNode != self._playerInfo.end:
            if (len(openNodes) == 0):
                return False
            
            currentNode = openNodes.popKey()
            closedNodes[currentNode] = None

            nextHexes: List[HexNode] = _tempGetAdjacentSpaces(currentNode)
            for nX in nextHexes:
                if not closedNodes.hasKey(nX) and not openNodes.hasKey(nX):
                    openNodes[nX] = None
            
        return True