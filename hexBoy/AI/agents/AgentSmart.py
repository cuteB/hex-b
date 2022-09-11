from typing import List

from hexBoy.AI.agentUtil.agentSmart.SmartChain import SmartChain
from hexBoy.AI.agentUtil.board.GetConnections import GetConnections
from hexBoy.AI.agentUtil.board.GetStrongMoves import GetStrongMoves
from hexBoy.AI.agentUtil.pathfinder.TrimPath import TrimEdgesFromPath
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.hex.game.HexGameRules import HexGameRules
from hexBoy.hex.node.HexNode import Hex
from hexBoy.pathfinder.PathBoy import PathBoy

'''----------------------------------
Agent Smart
----------------------------------'''
class AgentSmart(HexAgent):
    """AgentSmart is so smart it can think two moves ahead"""
    _chain: SmartChain = None
    _pf: PathBoy

    def __init__(self):
        HexAgent.__init__(self, "Agent_Smart")

    # Override
    def getAgentMove(self) -> Hex:
        agentMoves: List[Hex] = self._gameBoard.getPlayerMoves(self._playerInfo.player)

        # Early Move (first move)
        if (len(agentMoves) == 0):
            if (self._gameBoard.validateMove((5,5))):
                # take middle move
                return (5,5)
            elif (self._playerInfo.player == 1):
                # blue
                if (self._gameBoard.validateMove((4,5))):
                    return (4,5)
            elif (self._playerInfo.player == 2):
                # red
                if (self._gameBoard.validateMove((5,6))):
                    return (5,6)

        # Mid Game
        (weakConnections, _) = GetConnections(self._gameBoard, self._playerInfo.player)
        self._chain.updateChain()
        bestPath = TrimEdgesFromPath(self._pf.findPath(self._playerInfo.start, self._playerInfo.end))

        strongMoves = GetStrongMoves(self._playerInfo.player, self._gameBoard)

        # fill in weak connections (can probs keep like this)
        if (len(weakConnections) > 0):
            for m in weakConnections:
                if (self._gameBoard.validateMove(m)):
                    return m

        # Check if end game, i think this is the right check
        if (len(bestPath) == self._chain.getLength()): 
            for X in self._chain.getConnections():
                if (self._gameBoard.validateMove(X)):
                    return X

        # return a potential chain move on the side with the farthest from the edge
        closestDist = self._gameBoard.boardSize
        closestPos = None
        if (self._chain.getStartDist() > self._chain.getEndDist()):
            # make start closer 
            pMoves = self._chain.getStartPotentialMoves()
        else: 
            pMoves = self._chain.getEndPotentialMoves()
        

        # look at strong moves first, ugly loops
        tDist = None
        for m in pMoves:
            if m in strongMoves:
                tDist = self._chain.getDistToEndZone(m)
                if (tDist < closestDist):
                    closestDist = tDist
                    closestPos = m
        # short moves next
        for m in pMoves:
            if m not in strongMoves:
                tDist = self._chain.getDistToEndZone(m)
                if (tDist < closestDist):
                    closestDist = tDist
                    closestPos = m
        
        if (self._gameBoard.validateMove(closestPos)): # should always be valid
            return closestPos

        # default random move
        return self._randomMove()

    # Override
    def setGameBoardAndPlayer(self, gameBoard, player) -> None:
        HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

        self._pf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._playerInfo.player), 
            HexGameRules.getHeuristicFunc(self._playerInfo.player)
        )

        self._chain = SmartChain(self._playerInfo.player, self._gameBoard)
