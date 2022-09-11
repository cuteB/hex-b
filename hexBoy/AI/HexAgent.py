import random
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Callable

from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.node.HexNode import Hex
from hexBoy.hex.game.HexGameRules import HexGameRules, HexPlayerInfo
from hexBoy.AI.agentUtil.board.SyncBoard import SyncBoard

'''----------------------------------
Hex Agent
----------------------------------'''
class HexAgent(ABC):
    """Hex Agent Base class"""
    _name: str
    _playerInfo: HexPlayerInfo
    _opponentInfo: HexPlayerInfo

    _gameBoard: HexBoard  
    _agentBoard: HexBoard

    _moveCallback: Callable[[int, Hex], None] = None # Callback function that allows agents to do something after each move

    def __init__(self, name):
        self._name = name

    '''---
    public
    ---'''
    @abstractmethod
    def getAgentMove(self) -> Hex:
        """Get the next move for the agent"""

    def scoreGame(self) -> None:
        """Score game and get good."""
        pass

    def updateBoard(self) -> None:
        """Board was updated, Agent should handle the new moves"""

        SyncBoard(self._agentBoard, self._gameBoard, self._moveCallback)

    def startGame(self) -> None:
        """Start the game and reset the board and other stuff"""

        self._agentBoard.resetGameBoard()

    def setGameBoardAndPlayer(self, gameBoard: HexBoard, player:int) -> None:  
        """Link the game board and setup the player info"""

        self._agentBoard = HexBoard()
        self._gameBoard = gameBoard
        self._playerInfo = HexGameRules.getPlayerInfo(player)
        self._opponentInfo = HexGameRules.getOpponentInfo(player)

    def getName(self) -> str:
        """Get Agent's name"""

        return self._name


    '''---
    private
    ---'''
    def _randomMove(self) -> Hex:
        """Make a random valid move"""

        gameBoard = self._gameBoard
        x = random.randint(0, gameBoard.boardSize - 1)
        y = random.randint(0, gameBoard.boardSize - 1)
        cell = (x, y)

        while not gameBoard.validateMove((x, y)):
            x = random.randint(0, gameBoard.boardSize - 1)
            y = random.randint(0, gameBoard.boardSize - 1)
            cell = (x, y)

        return cell
