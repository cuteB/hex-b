from hexBoy.hex.HexBoard import Board
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.AI.agentUtil.agentSmart.GetConnections import GetConnections
from hexBoy.AI.agentUtil.agentSmart.GetStrongMoves import GetStrongMoves
from hexBoy.AI.agentUtil.agentSmart.SmartChain import SmartChain
from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.models.SortedDict import SortedDict

'''----------------------------------
Agent Smart
----------------------------------'''
class AgentSmart(HexAgent):
    hexValues: SortedDict = None
    chain: SmartChain = None

    # AgentSmart thinks two moves ahead
    def __init__(self):
        HexAgent.__init__(self)
        self.name = "Agent_Smart"

    '''---
    Agent Functions (Overrides)
    ---'''
    def getAgentMove(self) -> tuple[int,int]:
        agentMoves = self.gameBoard.getPlayerMoves(self.player)

        # Early Move (first move)
        if (len(agentMoves) == 0):
            if (self.gameBoard.validateMove((5,5))):
                # take middle move
                return (5,5)
            elif (self.player == 1):
                # blue
                if (self.gameBoard.validateMove((4,5))):
                    return (4,5)
            elif (self.player == 2):
                # red
                if (self.gameBoard.validateMove((5,6))):
                    return (5,6)

        # Mid Game
        (weakConnections, strongConnections) = GetConnections(self.gameBoard, self.player)
        self.chain.updateChain()
        bestPath = self.pathfinder.findPath(self.startPos, self.endPos)
        strongMoves = GetStrongMoves(self.gameBoard, self.player)

        # fill in weak connections (can probs keep like this)
        if (len(weakConnections) > 0):
            for m in weakConnections:
                if (self.gameBoard.validateMove(m)):
                    return m

        # Check if end game, i think this is the right check
        if (len(bestPath) == self.chain.length): 
            for X in self.chain.connections:
                if (self.gameBoard.validateMove(X)):
                    return X

        # return a potential chain move on the side with the farthest from the edge
        closestDist = self.gameBoard.boardSize
        closestPos = None
        if (self.chain.startDist > self.chain.endDist):
            # make start closer 
            pMoves = self.chain.getStartPotentialMoves()
        else: 
            pMoves = self.chain.getEndPotentialMoves()
        

        # look at strong moves first, ugly loops
        tDist = None
        for m in pMoves:
            if m in strongMoves:
                tDist = self.chain.getDistToEndZone(m)
                if (tDist < closestDist):
                    closestDist = tDist
                    closestPos = m
        # short moves next
        for m in pMoves:
            if m not in strongMoves:
                tDist = self.chain.getDistToEndZone(m)
                if (tDist < closestDist):
                    closestDist = tDist
                    closestPos = m

        
        if (self.gameBoard.validateMove(closestPos)): # should always be valid
            return closestPos

        # default random move
        return self._randomMove()

    # Override
    def setGameBoardAndPlayer(self, gameBoard, player):
        HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

        self.pathfinder = PathBoy(
            self.gameBoard,
            self.getAdjacentSpaces,
            self.checkIfBarrier,
        )

        self.chain = SmartChain(self.player, self.gameBoard)

    