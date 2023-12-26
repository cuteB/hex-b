import random
from typing import List

from hexBoy.AI.HexAgent import HexAgent
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.game.HexGameRules import HexGameRules
from hexBoy.hex.node.HexNode import Hex
from hexBoy.pathfinder.PathBoy import PathBoy

'''----------------------------------
AStar Search Agent
----------------------------------'''
class AgentAStar(HexAgent):
    """Hex Agent that uses A* path finding to get the next move"""
    _pf: PathBoy

    def __init__(self):
        HexAgent.__init__(self, "Agent_A*")

        self._moveCallback = self.pathMoveCallback

    # Override
    def getAgentMove(self) -> Hex:
        # Find best path to win
        potentialMoves: List[Hex] = self._pf.findPath(
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
    def setGameBoardAndPlayer(self, gameBoard: HexBoard, player: int) -> None:
        HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

        # AStar Pathfinder
        self._pf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._playerInfo.player), 
            HexGameRules.getHeuristicFunc(self._playerInfo.player)
        )

    def pathMoveCallback(self, player: int, X: Hex) -> None:
        self._pf.findPath(
            self._playerInfo.start,
            self._playerInfo.end,
        )
