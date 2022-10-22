import math
from typing import Callable, Dict, List, Tuple

from hexBoy.hex.board.HexBoard import Board, HexBoard
from hexBoy.hex.game.HexGameRules import HexGameRules, HexPlayerInfo
from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.node.HexNode import Hex, HexNode
from hexBoy.models.SortedDict import SortedDict

class NumPathFinder(PathBoy):

    # TODO remove from pathboy. A* ruins the num path algorithm
    _playerInfo: HexPlayerInfo

    _clusterId: int = 0
    _clusters: SortedDict # int -> List[Hex]    
    _hexToCluster: SortedDict # Hex -> int

    def __init__(
        self,
        board: Board,
        player: int
    ):
        PathBoy.__init__(self, 
            board,
            checkIfBarrier=HexGameRules.getCheckIfBarrierFunc(player),
            heuristicFunc=HexGameRules.getHeuristicFunc(player)
        )

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
                if aX not in clusterHexes and aX not in adjHexesToCluster:
                    adjHexesToCluster.append(aX)

        return adjHexesToCluster




    def initEmptyBoard(self) -> None:

        board = self._board

        # Init all the nodes with their costs and family
        nodes: Dict[Hex, HexNode] = board.getNodeDict()
        adjacentSpaces: List[Hex] = None
        nextNode: Hex = None

        # sort by heur. go row by row 
        def sortFunc(item: Tuple[HexNode, HexNode]) -> int:
            return self._heuristicFunc(item[1], None)

        def _scoreNode(X: HexNode) -> None:
            """Score PCD and set initial family"""

            h = self._heuristicFunc(X, None)
            X.setPath(max(11 - h, 0)) # end zones return -1 with heur
            X.setDist(max(h - 1, 0))
            X.setHeur(h - 1)

            if (X.getHexType().xType == 1):
                # Playable board
                # Set dads/sons 
                for aX in board.getAdjacentSpaces(X): # Sometimes using board sometimes self._board
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

            if (len(X.getDads()) == 0):
                # Edges with no dads have 1 path
                X.setPathsToNode(1)

            else:
                num = 0
                for dad in X.getDads():
                    num += dad.getPathsToNode()
                X.setPathsToNode(num)

        openNodes: SortedDict = SortedDict(getSortValue=sortFunc, reverse=True)
        closedNodes: SortedDict = SortedDict()

        currentNode: HexNode = self._playerInfo.start
        openNodes[currentNode] = nodes[currentNode]

        while (len(openNodes) != 0):
            currentNode = openNodes.pop()
            closedNodes[currentNode] = None
            _scoreNode(currentNode)
            
            adjacentSpaces = self._board.getAdjacentSpaces(currentNode)            
            for nextPos in adjacentSpaces:
                nextNode = nodes[nextPos]

                if not self._checkIfBarrier(nextNode) and not closedNodes.hasKey(nextPos) and not openNodes.hasKey(nextPos):
                    nodes[nextNode] = nextNode
                    openNodes[nextNode] = nextNode

        # Go backward
        openNodes = SortedDict(getSortValue=sortFunc)
        closedNodes = SortedDict()

        currentNode = self._playerInfo.end
        openNodes[currentNode] = nodes[currentNode]

        def _setPathsFrom(X: HexNode) -> None:
            # TODO
            if (len(X.getSons()) == 0):
                # Edges with no sons have 1 path
                X.setPathsFromNode(1)

            else:
                num = 0
                for son in X.getSons():
                    num += son.getPathsFromNode()
                X.setPathsFromNode(num)

        while (len(openNodes) != 0):
            currentNode = openNodes.pop()
            closedNodes[currentNode] = None
            _setPathsFrom(currentNode)

            adjacentSpaces = self._board.getAdjacentSpaces(currentNode)            
            for nextPos in adjacentSpaces:
                nextNode = nodes[nextPos]

                if not self._checkIfBarrier(nextNode) and not closedNodes.hasKey(nextPos) and not openNodes.hasKey(nextPos):
                    openNodes[nextNode] = nextNode


    def updateMove(self, player: int, move: Hex) -> None:
        """Update board with the new move"""

        nodes: Dict[Hex, HexNode] = self._board.getNodeDict()
        X: HexNode = nodes[move]

        def _sortFunc(item: Tuple[HexNode, int]) -> int:
            return item[1]

        # Helper functions

        def _updateNode(X: HexNode) -> None:

            if (X.getHexType().xType == 2): 
                # Edge
                return

            # get Adjacent Hexes            
            adjSpaces: List[Hex]
            if (X.getHexType().player == self._playerInfo.player):
                # player move, use cluster's adjacent hexes as nodes adjHexes
                adjSpaces: List[Hex] = self._getClusterAdjacentSpaces(self._hexToCluster[X])
            else:
                # regular hex
                adjSpaces: List[Hex] = self._board.getAdjacentSpaces(X)
            adjHexes: List[HexNode] = list(map(lambda X: nodes[X], adjSpaces)) 



            # Get best dads and sons costs
            bestDadPC: int = -1
            bestSonCD: int = -1
            for aX in adjHexes:
                if (not self._checkIfBarrier(aX)):
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
                    nextDads = [d]
                    break

                elif d in self._hexToCluster.getKeys():
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
                    # end zone
                    nextSons = [s]
                    break

                elif s in self._hexToCluster.getKeys():
                    cId: int = self._hexToCluster[s]
                    if cId not in sonClusters:
                        sonClusters.append(cId)
                        nextSons.append(s)
                
                else:
                    nextSons.append(s)

            X.setDads(nextDads)
            X.setSons(nextSons)

            X.setPath(X.getDad().getPC())
            X.setDist(X.getSon().getCD())
            nodes[X] = X




        def _updateNodePathsTo(X: HexNode) -> None:
            """Update node's dads, path, and paths to node"""

            if (X.getHexType().xType == 2): # Edge
                return

            dads: List[HexNode] = X.getDads()
            pathsToNode = 0
            for d in dads:
                pathsToNode += d.getPathsToNode()

            # Update node and nodes
            X.setPathsToNode(pathsToNode)
            nodes[X] = X



        def _updateNodePathsFrom(X: HexNode) -> None:
            """Update node's sons, dist and paths from node"""

            if (X.getHexType().xType == 2): # Edge
                return

            sons: List[HexNode] = X.getSons()
            pathsFromNode = 0
            for s in sons:
                pathsFromNode += s.getPathsFromNode()

            # Update node and nodes
            X.setPathsFromNode(pathsFromNode)
            nodes[X] = X

        # Handle player move
        if (player == self._playerInfo.player):
            # player move
            adjClusters: List[int] = []
            for aX in self._board.getAdjacentSpaces(move):
                if aX in self._hexToCluster.getKeys():
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
            # opp move
            for s in X.getSons():
                s.delDad(X)

            for d in X.getDads():
                d.delSon(X)

        # Update family
        openNodes = SortedDict(getSortValue=_sortFunc)
        closedNodes = SortedDict()
        pathDepth = SortedDict(getSortValue=_sortFunc)
        
        openNodes[X] = 0 # Breadth first 
        pathDepth[X] = 0

        currentNode: HexNode
        order: int
        while (len(openNodes) != 0):
            currentNode, order = openNodes.popItem()
            closedNodes[currentNode] = None
            depth = pathDepth[currentNode]

            currentNode = nodes[currentNode]
            

            _updateNode(currentNode) # Family is set

            sons: List[HexNode] = currentNode.getSons()
            dads: List[HexNode] = currentNode.getDads()
            cluster: List[HexNode] = []
            if (currentNode in self._hexToCluster.getKeys()):
                cluster = self._clusters[self._hexToCluster[currentNode]]

            # Add nodes family/neighbours to open
            # Go through existing hex cluster first
            for cX in cluster:
                if (not openNodes.hasKey(cX) and not closedNodes.hasKey(cX)):
                    openNodes[cX] = order
                    pathDepth[cX] = depth

            # Go through family
            # - sons/dads that are taken hexes have a 0.5 depth difference so they go before empty hexes 
            for sX in sons:
                if (not openNodes.hasKey(sX) and not closedNodes.hasKey(sX)):
                    openNodes[sX] = order + 1
                    
                    if sX.getHexType().player == self._playerInfo.player: # Player hex
                        pathDepth[sX] = math.floor(depth) + 0.5
                    
                    else: 
                        pathDepth[sX] = math.floor(depth) + 1 

            for dX in dads:
                if (not openNodes.hasKey(dX) and not closedNodes.hasKey(dX)):
                    openNodes[dX] = order + 1

                    if dX.getHexType().player == self._playerInfo.player: # Player hex
                        pathDepth[dX] = math.floor(depth) - 0.5
                    
                    else: 
                        pathDepth[dX] = math.floor(depth) - 1


        # update paths to/from
        openNodes = SortedDict(initDict=pathDepth, getSortValue=_sortFunc)
        closedNodes = SortedDict()

        while (len(openNodes) != 0):
            currentNode, _ = openNodes.popItem()
            closedNodes[currentNode] = None
            currentNode = nodes[currentNode]

            _updateNodePathsTo(currentNode)


        # update paths From
        openNodes = SortedDict(initDict=pathDepth, getSortValue=_sortFunc, reverse=True)
        closedNodes = SortedDict()

        openNodes[nodes[move]] = 0

        while (len(openNodes) != 0):
            currentNode, _ = openNodes.popItem()
            closedNodes[currentNode] = None
            currentNode = nodes[currentNode]

            _updateNodePathsFrom(currentNode)


    def getNumPaths(self) -> int:
        """Get the total number of paths that have the best cost"""
        bestBest: int = -1
        numPaths: int = 0

        nodes: Dict[Hex, HexNode] = self._board.getNodeDict()
        openNodes = SortedDict()
        closedNodes = SortedDict()

        currentNode = self._playerInfo.end
        openNodes[currentNode] = nodes[currentNode]

        while (len(openNodes) != 0):
            currentNode: HexNode = openNodes.pop()
            closedNodes[currentNode] = None

            if (currentNode.getDad().getBest() < bestBest or bestBest == -1):
                bestBest = currentNode.getDad().getBest()

            adjacentSpaces = self._board.getAdjacentSpaces(currentNode)            
            for nextPos in adjacentSpaces:
                nextNode = nodes[nextPos]

                if (not self._checkIfBarrier(nextNode) and not closedNodes.hasKey(nextPos) and not openNodes.hasKey(nextPos)
                    and nextNode.getHexType().xType == 2
                ):
                    openNodes[nextNode] = nextNode

        for X in closedNodes.getKeys():
            dad: HexNode = X.getDad()
            if (dad.getBest() == bestBest):
                numPaths += dad.getPathsToNode()

        return numPaths

    def getNumPathsToHex(self, X: Hex) -> int:
        """Get the number of paths to a given hex"""

        node: HexNode = self._board.getNodeDict()[X]
        return node.getPathsToNode()

    def getNumPathsFromHex(self, X: Hex) -> int:
        """Get the number of paths from a given Hex"""

        node: HexNode = self._board.getNodeDict()[X]
        return node.getPathsFromNode()

    """
    '''---
    Best paths
    ---'''
    def old_numBestPaths(self, nodes, startPos, endPos, checkIfBarrier):
        nodes = self._board.getNodeDict(),
        spaces = HexNode.SpaceTypes
        numPaths = SortedDict()

        winPath = self._AStar(startPos, endPos)
        bestCost = self.scorePath(winPath)

        openNodes = SortedDict(getSortValue=self.getSortValue)
        closedNodes = SortedDict()
        endNodes = SortedDict()  # nodes to add up to get the number of paths

        # add starting position to pop off
        currentPos = startPos # maybe rename Pos to Hex
        currentNode = nodes[currentPos]
        currentNode.setExtraPathsToNode(0.25)
        openNodes[currentPos] = currentNode

        adjacentSpaces = None
        nextNode = None
        closedNode = None

        # helper functions
        def setNodeInOpenNodes(pos):
            nextNode.scoreHeuristic(currentPos, currentNode.getPC(), endPos)
            nonlocal numPaths

            # check if this pos is on the winning edge and moving from a non edge
            # to an end edge
            if (
                (nextNode.type == spaces.BLUE_EDGE or nextNode.type == spaces.RED_EDGE)
                and (
                    currentNode.type != spaces.BLUE_EDGE
                    or currentNode.type != spaces.RED_EDGE
                )
                and nextNode.getPC() == bestCost
            ):
                # node is an edge and has the best cost -> is a winning path
                # add paths to the total paths
                if currentNode.extraPathsToThisNode != 0:
                    numPaths[currentPos] = currentNode.extraPathsToThisNode

            # moving from start edge to playable board
            elif (
                nextNode.type != spaces.BLUE_EDGE or nextNode.type != spaces.RED_EDGE
            ) and (
                currentNode.type == spaces.BLUE_EDGE
                or currentNode.type == spaces.RED_EDGE
            ):
                nextNode.setExtraPathsToNode(1)

            else:
                nextNode.setExtraPathsToNode(currentNode.extraPathsToThisNode)

            nodes[pos] = nextNode
            openNodes[pos] = nextNode

        def updateNodeInOpenNodes(pos):
            nonlocal numPaths

            # check if it is a # check if it is a what?
            if (
                (nextNode.type == spaces.BLUE_EDGE or nextNode.type == spaces.RED_EDGE)
                and (
                    currentNode.type != spaces.BLUE_EDGE
                    or currentNode.type != spaces.RED_EDGE
                )
                and nextNode.getPC() == bestCost
            ):
                if currentNode.extraPathsToThisNode != 0:
                    numPaths[currentPos] = currentNode.extraPathsToThisNode

            # moving from start edge to playable board
            elif (
                nextNode.type != spaces.BLUE_EDGE or nextNode.type != spaces.RED_EDGE
            ) and (
                currentNode.type == spaces.BLUE_EDGE
                or currentNode.type == spaces.RED_EDGE
            ):
                nextNode.setExtraPathsToNode(1)

            else:
                openNodes[pos].addExtraPathsToNode(currentNode.extraPathsToThisNode)

        # gotta loop through everything
        while len(openNodes) > 0:
            currentNode = openNodes.popKey()
            closedNodes[currentNode] = None

            adjacentSpaces = self.getAdjacentSpaces(currentNode)
            for nextPos in adjacentSpaces:
                nextNode = nodes[nextPos]

                if not checkIfBarrier(nextNode) and not closedNodes.hasKey(nextPos):
                    if (currentNode.getPC() + nextNode.cost) > bestCost:
                        # Too expensive
                        pass

                    elif nextPos == endPos:
                        # Path Found
                        pass

                    elif openNodes.hasKey(nextPos):
                        # In open nodes. check cost compared to this path
                        if nextNode.getPC() > currentNode.getPC() + nextNode.cost:
                            # new path better. Overwrite and set path
                            setNodeInOpenNodes(nextPos)

                        elif nextNode.getPC() == currentNode.getPC() + nextNode.cost:
                            # same path same cost. add paths to node
                            updateNodeInOpenNodes(nextPos)

                    else:
                        # not in open nodes
                        setNodeInOpenNodes(nextPos)

        # return paths
        total = 0
        ez = [] #  remove if not used
        while len(numPaths) > 0:
            num = numPaths.pop()
            ez.append(num)
            total += num
        return total
        
    """
