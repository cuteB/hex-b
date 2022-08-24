from typing import List
from hexBoy.models.SortedDict import SortedDict
from hexBoy.hex.HexBoard import Board
from hexBoy.AI.agentUtil.agentSmart.GetConnections import GetConnections

'''----------------------------------
Smart Chain
----------------------------------'''
# Assuming that the hexes are all in one chain due to the agent's game plan. 

class SmartChain():
    """A chain that links hexes that have a connection on a board"""
    board: Board
    player: int = None

    linkedDict: SortedDict = None
    connections: List[tuple] = None
    startPos: tuple = None
    endPos: tuple = None
    startDist: int = None
    endDist: int = None
    length: int = None

    def __init__(self, _player: int, _board: Board):
        self.board = _board
        self.player = _player

        self.connections = []
        self.linkedDict = SortedDict()
        self.length = 0

        # update chain based on board
        self.updateChain()

    '''---
    Public
    ---'''
    def updateChain(self):
        playerMoves = self.board.getPlayerMoves(self.player)
        (_, strongConnections) = GetConnections(self.board, self.player)





