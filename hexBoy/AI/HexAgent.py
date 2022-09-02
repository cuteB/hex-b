""" #TODO this bit can probably move from the ABC
Save RL agent to keep smart?
- Store best as a greedy agent

Think about composition and inheritance.
- Pathfinders seem to fall into categories that they can use.
- Do a better initialize maybe.
  - Need to initialize board or get move doesn't work
  - Maybe just check if the board hasn't been initialized.
"""

import random
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

from hexBoy.hex.board.HexBoard import Board
from hexBoy.hex.node.HexNode import HexNode

"""----------------------------------
Hex Agent
----------------------------------"""

@dataclass
class HexAgent(ABC):
    # TODO descriptions
    name: str
    player: int  # 1: blue or 2: red

    # Board
    gameBoard: Board  # TODO These will use Hexboard
    agentBoard: Board
    getAdjacentSpaces = None  # TODO remove and use gameBoard.getAdjacentSpaces

    # pathfinder: player positions and barrier checks
    startPos = None  # player start
    endPos = None  # player end
    opponentStart = None
    opponentEnd = None
    checkIfBarrier = (
        None  # player barriers # TODO These functions might change up a bit
    )
    checkIfOpponentBarrier = None  # opponent barriers
    moveCallback = None  # TODO give this a description

    def __init__(self):
        # TODO I feel like a bunch of values can be defined here such as name and player start spaces too but player is set in setGameBoardAndPlayer so maybe not
        # TODO defs set player here
        pass  # nothing for now

    @abstractmethod
    def getAgentMove(self) -> tuple: # TODO check if I need descriptions for each of the inherited functions
        """Get the next move for the agent"""

    def scoreGame(self):
        """Score game and get good."""
        return

    def updateBoard(self):
        """Board was updated, Agent should handle the new moves"""
        self.agentBoard.syncBoard(self.gameBoard, self.moveCallback)

    def startGame(self):
        """Start the game and reset the board and other stuff"""
        self.agentBoard.resetGame()

    # Init board and player
    def setGameBoardAndPlayer(self, gameBoard, player): # TODO I think this is private
        self._initGameBoard(gameBoard)
        self._initPlayerBoard(player)

    '''---
    Agent Setup
    ---'''

    # TODO These two functions are basically the same. should probably combine unless an agent has a good reason do something differen
    def _initGameBoard(self, gameBoard):
        self.agentBoard = Board(gameBoard.boardSize)
        self.gameBoard = gameBoard
        self.getAdjacentSpaces = gameBoard.getAdjacentSpaces

    def _initPlayerBoard(self, player):
        self.player = player
        gameBoard = self.gameBoard

        # TODO again this needs to change. It is everywhere
        # Blue player
        if self.player == 1:
            self.startPos = gameBoard.blueStartSpace
            self.endPos = gameBoard.blueEndSpace
            self.opponentStart = gameBoard.redStartSpace
            self.opponentEnd = gameBoard.redEndSpace
            self.checkIfBarrier = HexNode.checkIfBlueBarrierForAI
            self.checkIfOpponentBarrier = HexNode.checkIfRedBarrierForAI

        # Red player
        else:
            self.startPos = gameBoard.redStartSpace
            self.endPos = gameBoard.redEndSpace
            self.opponentStart = gameBoard.blueStartSpace
            self.opponentEnd = gameBoard.blueEndSpace
            self.checkIfBarrier = HexNode.checkIfRedBarrierForAI
            self.checkIfOpponentBarrier = HexNode.checkIfBlueBarrierForAI

    '''---
    Random Move
    ----'''

    def _randomMove(self):
        gameBoard = self.gameBoard
        x = random.randint(0, gameBoard.boardSize - 1)
        y = random.randint(0, gameBoard.boardSize - 1)
        cell = (x, y)

        while not gameBoard.validateMove((x, y)):
            x = random.randint(0, gameBoard.boardSize - 1)
            y = random.randint(0, gameBoard.boardSize - 1)
            cell = (x, y)

        return cell
