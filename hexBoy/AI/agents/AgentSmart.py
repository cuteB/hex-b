from hexBoy.hex.HexBoard import Board
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.AI.agentUtil.agentSmart.GetConnections import GetConnections
from hexBoy.AI.agentUtil.agentSmart.GetStrongMoves import GetStrongMoves
from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.models.SortedDict import SortedDict

'''----------------------------------
Agent Smart
----------------------------------'''
class AgentSmart(HexAgent):
    # AgentSmart thinks two moves ahead
    def __init__(self):
        HexAgent.__init__(self)
        self.name = "Agent_Smart"

    '''---
    Agent Functions (Overrides)
    ---'''
    def getAgentMove(self) -> tuple[int,int]:
        # get best path.
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

        # fill in weak connections
        if (len(weakConnections) > 0):
            for m in weakConnections:
                if (self.gameBoard.validateMove(m)):
                    return m

        strongMoveValues = SortedDict()
        strongMoves = GetStrongMoves(self.gameBoard, self.player)
        # make a move that is closest to the edge of the board
        for sm in strongMoves:
            strongMoveValues[sm] = self.getDistanceToClosestEdge(sm)

        for sm in strongMoveValues.getKeys():
            if self.gameBoard.validateMove(sm):
                return sm``

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

    def getDistanceToClosestEdge(self, hex):
        if (self.player == 1): # blue
            val = hex[1]
        else:
            val = hex[0]

        if (val <= 5):
            return val
        else: 
            return 10 - val