import random

from hexBoy.hex.game.HexGameRules import HexGameRules
from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.AI.agentUtil.eval.MoveEval import evaluateMove

'''----------------------------------
Strong move Agent
----------------------------------'''

class AgentStrong(HexAgent):
    _pf: PathBoy
    _opf: PathBoy

    def __init__(self):
        HexAgent.__init__(self, "Agent_Strong")

    '''---
    Agent Functions
    ---'''
    # Override
    def getAgentMove(self):
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

        def sortFunc(item):
            return item[1].getPC()

        self._pf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._playerInfo.player), 
            HexGameRules.getHeuristicFunc(self._playerInfo.player), 
            sortFunc
        )

        self._opf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._opponentInfo.player), 
            HexGameRules.getHeuristicFunc(self._opponentInfo.player), 
            sortFunc
        )
