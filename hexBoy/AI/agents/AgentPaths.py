import random
from typing import List

from hexBoy.AI.HexAgent import HexAgent
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.game.HexGameRules import HexGameRules
from hexBoy.hex.node.HexNode import Hex
from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.pathfinder.NumPathFinder import NumPathFinder

'''----------------------------------
AStar Search Agent
----------------------------------'''
class AgentPaths(HexAgent):
    """Hex Agent that uses A* path finding to get the next move"""
    _pf: PathBoy
    _npf: NumPathFinder

    def __init__(self):
        HexAgent.__init__(self, "Agent_A*")
        self._moveCallback = self.pathMoveCallback


    # Override
    def startGame(self) -> None:
        HexAgent.startGame(self)
        self._npf.initEmptyBoard()

    # Override
    def getAgentMove(self) -> Hex:
        # Find best path to win

        return self._randomMove()

    # Override
    def setGameBoardAndPlayer(self, gameBoard: HexBoard, player: int) -> None:
        HexAgent.setGameBoardAndPlayer(self, gameBoard, player)
        
        self._npf = NumPathFinder(
            self._agentBoard,
            player
        )

        self._npf.initEmptyBoard() # Might not need this one because initEmptyBoard is in startGame()

    def pathMoveCallback(self, player: int, X: Hex) -> None:
        self._npf.updateMove(player, X)