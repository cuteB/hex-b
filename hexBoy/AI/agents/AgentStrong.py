from typing import Tuple
from hexBoy.AI.agentUtil.eval.MoveEval import evaluateMove
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.hex.game.HexGameRules import HexGameRules
from hexBoy.hex.node.HexNode import Hex
from hexBoy.pathfinder.PathBoy import PathBoy

'''----------------------------------
Strong move Agent
----------------------------------'''
class AgentStrong(HexAgent):
    """Make moves that might be strong. Not very smart"""
    _pf: PathBoy
    _opf: PathBoy

    def __init__(self):
        HexAgent.__init__(self, "Agent_Strong")

    # Override
    def getAgentMove(self) -> Hex:
        gameBoard = self._gameBoard

        winPath = self._pf.findPath(
            self._playerInfo.start,
            self._playerInfo.end,
        )

        opponentPath = self._opf.findPath(
            self._opponentInfo.start,
            self._opponentInfo.end,
        )

        move = self._randomMove()
        moveVal = evaluateMove(move, gameBoard, winPath, opponentPath, self._playerInfo.player)

        for x in range(gameBoard.boardSize):
            for y in range(gameBoard.boardSize):
                nextMove = (x, y)
                if gameBoard.validateMove(nextMove):
                    nextVal = evaluateMove(
                        nextMove, gameBoard, winPath, opponentPath, self._playerInfo.player
                    )
                    if nextVal > moveVal:
                        moveVal = nextVal
                        move = nextMove

        return move

    # Override
    def setGameBoardAndPlayer(self, gameBoard, player):
        HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

        self._pf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._playerInfo.player), 
            HexGameRules.getHeuristicFunc(self._playerInfo.player)
        )

        self._opf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._opponentInfo.player), 
            HexGameRules.getHeuristicFunc(self._opponentInfo.player),
        )
