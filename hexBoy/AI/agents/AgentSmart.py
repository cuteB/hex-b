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
    hexValues: SortedDict = None

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

        def sortFunc(val): return val[1]
        strongMoveValues = SortedDict(getSortValue=sortFunc, reverse=True)
        strongMoves = GetStrongMoves(self.gameBoard, self.player)
        # make a move that is closest to the edge of the board
        for sm in strongMoves:
            strongMoveValues[sm] = self.hexValues[sm]

        for sm in strongMoveValues.getKeys():
            if self.gameBoard.validateMove(sm):
                return sm

        # default random move
        return self._randomMove()

    # Override
    def setGameBoardAndPlayer(self, gameBoard, player):
        HexAgent.setGameBoardAndPlayer(self, gameBoard, player)
        self._initHexValueDict()

        self.pathfinder = PathBoy(
            self.gameBoard,
            self.getAdjacentSpaces,
            self.checkIfBarrier,
        )

    def _initHexValueDict(self):
        def _getDistanceToClosestPlayerEdge(hex):
            if (self.player == 1): # blue
                val = hex[1]
            else:
                val = hex[0]

            if (val <= 5):
                return val
            else: 
                return 10 - val

        self.hexValues = SortedDict()

        # value multipliers for each distance
        lambdaCenter =  0.8
        lambdaEdge = 0.5
        boardSize = self.gameBoard.boardSize

        for x in range(boardSize):
            for y in range(boardSize):
                X = (x,y)
                distToCenter = self.gameBoard.getDistanceToCenter(X)
                distToEdge = _getDistanceToClosestPlayerEdge(X)

                val = (lambdaCenter * (boardSize - distToCenter)) + (lambdaEdge * (boardSize - distToEdge))

                self.hexValues[X] = val