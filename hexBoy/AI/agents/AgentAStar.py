import random

from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.hex.game.HexGameRules import HexGameRules

'''----------------------------------
AStar Search Agent
----------------------------------'''
class AgentAStar(HexAgent):
    """Hex Agent that uses A* path finding to get the next move"""
    _pf: PathBoy

    def __init__(self):
        HexAgent.__init__(self, "Agent_A*")

    # Override
    def getAgentMove(self):
        # Find best path to win
        potentialMoves = self._pf.findPath(
            self._playerInfo.start,
            self._playerInfo.end,
        )

        # make a move on the best path
        random.shuffle(potentialMoves)
        for move in potentialMoves:
            if self._gameBoard.validateMove(move):
                return move

        return self._randomMove()

    # Override
    def setGameBoardAndPlayer(self, gameBoard: HexBoard, player: int):
        HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

        def sortFunc(item):
            return item[1].getPC()

        # AStar Pathfinder
        self._pf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._playerInfo.player), 
            HexGameRules.getHeuristicFunc(self._playerInfo.player)
        )
