""" #TODO this bit can probably move from the ABC
Think about composition and inheritance.
- Pathfinders seem to fall into categories that they can use.
- Do a better initialize maybe.
  - Need to initialize board or get move doesn't work
  - Maybe just check if the board hasn't been initialized.
"""

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
    name: str
    _playerInfo: HexPlayerInfo
    _opponentInfo: HexPlayerInfo

    # Board
    _gameBoard: HexBoard  
    _agentBoard: HexBoard

    _moveCallback: Callable[[int, Hex], None] = None # Callback function that allows agents to do something for each move

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def getAgentMove(self) -> Hex:
        """Get the next move for the agent"""

    def scoreGame(self) -> None:
        """Score game and get good."""
        return

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


    '''---
    Random Move
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
