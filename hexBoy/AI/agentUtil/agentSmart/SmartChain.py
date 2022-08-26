from typing import List
from hexBoy.models.SortedDict import SortedDict
from hexBoy.hex.HexNode import HexNode
from hexBoy.hex.HexBoard import Board
from hexBoy.AI.agentUtil.agentSmart.GetConnections import GetConnections
from hexBoy.pathfinder.PathBoy import PathBoy

'''----------------------------------
Smart Chain
----------------------------------'''
# Assuming that the hexes are all in one chain due to the agent's game plan. 
# - Can defs do dynamic programming and update one move at a time to save time

class SmartChain():
    """A chain that links hexes that have a connection on a board"""
    board: Board
    player: int = None

    pathfinder: PathBoy
    linkedDict: SortedDict = None
    connections: List[tuple] = None
    startPos: tuple = None
    endPos: tuple = None
    startDist: int = None
    endDist: int = None
    length: int = None

    playerStart: tuple = None
    playerEnd: tuple = None

    def __init__(self, _player: int, _board: Board):
        self.board = _board
        self.player = _player

        if (self.player == 1):
            # blue
            self.playerStart = self.board.blueStartSpace
            self.playerEnd = self.board.blueEndSpace
            self.checkIfBarrier = HexNode.checkIfBlueBarrierForAI
            self.checkIfOpponentBarrier = HexNode.checkIfRedBarrierForAI
        else:
            # red
            self.playerStart = self.board.redStartSpace
            self.playerEnd = self.board.redEndSpace
            self.checkIfBarrier = HexNode.checkIfRedBarrierForAI
            self.checkIfOpponentBarrier = HexNode.checkIfBlueBarrierForAI
            

        self.connections = []
        self.linkedDict = SortedDict()
        self.length = 0

        def sortFunc(item):
            return item[1].path
        self.pathfinder = PathBoy(
            self.board,
            self.board.getAdjacentSpaces,
            self.checkIfBarrier,
            sortFunc
        )

        # update chain based on board
        self.updateChain()

    def getDistToEndZone(self, X):
        """"Get distance to closest player endZone (i think this exists somewhere)"""

        if (self.player == 1):
            # blue, compare y
            val = X[1]
        else:
            # red, compare x
            val = X[0]

        # assume board size 11
        if (val <= 5):
            return val + 1
        else:
            return 11 - val

    '''---
    Public
    ---'''
    def updateChain(self):
        """Look at the board and get the chain"""
        playerMoves = self.board.getPlayerMoves(self.player)
        (weakConnections, strongConnections) = GetConnections(self.board, self.player)
        allConnections = [*weakConnections, *strongConnections]
        nMoves = len(playerMoves)

        # No moves
        if (nMoves == 0):
            return
        
        # start with the first move and work both directions
        m = playerMoves[0]
        self.startPos = m
        self.endPos = m
        self.length = 1
        self.startDist = self.pathfinder.ScorePath(self.pathfinder.findPath(self.playerStart, m))
        self.endDist = self.pathfinder.ScorePath(self.pathfinder.findPath(self.playerEnd, m))

        nodes = [m]
        visited = []
        t = 0
        while (len(nodes) > 0):
            t += 1
            if t == 5:
                return

            m = nodes.pop()
            visited.append(m)
            print(m)

            adjacentHexes = self.board.getAdjacentSpaces(m)
            for aX in adjacentHexes:
                # adjacent move
                if (aX in playerMoves and aX not in visited):
                    nodes.append(aX)
                    distToStart = len(self.pathfinder.findPath(self.playerStart, aX))
                    distToEnd = len(self.pathfinder.findPath(self.playerEnd, aX))

                    # if move is closer to start
                    print(m, distToStart, self.startDist, self.getDistToEndZone(aX), self.getDistToEndZone(self.startPos))

                    if (
                        (distToStart < self.startDist)
                        or (distToStart == self.startDist and self.getDistToEndZone(aX) < self.getDistToEndZone(self.startPos))
                    ):
                        self.startPos = aX
                        self.startDist = distToStart
                        self.length += 1

                    # if move is closer to end\
                    print(m, distToEnd, self.endDist, self.getDistToEndZone(aX), self.getDistToEndZone(self.endPos))
                    if (
                        (distToEnd < self.endDist)
                        or (distToEnd == self.endDist and self.getDistToEndZone(aX) < self.getDistToEndZone(self.endPos))
                    ):
                        self.endPos = aX
                        self.endDist = distToEnd
                        self.length += 1
                
                
            



        













