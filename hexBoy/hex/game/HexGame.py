# I don't like the pygame startup message.
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import sys
from dataclasses import dataclass
from pygame.locals import *
from typing import List

from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.node.HexNode import HexNode, Hex
from hexBoy.hex.graphics.HexGraphics import HexGraphics
from hexBoy.hex.game.HexGameRules import HexGameRules
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.AI.HexAgent import HexAgent

# Custom Events
BEFORE_TURN = pygame.USEREVENT + 1
PLAYER_TURN = pygame.USEREVENT + 2
AFTER_TURN = pygame.USEREVENT + 3

# Game options
@dataclass
class HexGameOptions:
    showDisplay: bool
    showPrint: bool
    showEndGame: bool # TODO this is sloppy. Sorta works with just one game
    alternateStartingPlayer: bool = True

'''----------------------------------
Main hex game class
----------------------------------'''
@dataclass
class HexGame:
    """The Hex Game. """
    _gameBoard: HexBoard  # Board, Hex Board Object #
    _options: HexGameOptions

    _currentPlayer: int  
    _gameInProgress: bool  
    _forceQuit: bool

    _winPath: List[Hex]  # the winning path

    _graphics: HexGraphics  # Render the game board
    _bluePathFinder: PathBoy  # Pathfinder, Algorithms to find paths
    _redPathfinder: PathBoy

    _blueAgent: HexAgent  # AIs for player, None = human
    _redAgent: HexAgent
    _gameNumber: int
    _blueWins: int
    _redWins: int

    _blueName: str 
    _redName: str

    _nextMove: tuple

    def __init__(
        self,
        agent1: HexAgent = None,
        agent2: HexAgent =None,
        gameOptions: HexGameOptions = HexGameOptions()
    ):
        pygame.init() # Needs to be first

        self._gameBoard = HexBoard()
        self._options = gameOptions
        self._currentPlayer = 1 

        self._gameInProgress = True  # game loop check
        self._forceQuit = False
        self._nextMove

        self._currentGameNumber = 1
        self._winPath = None
        self._blueWins = 0
        self._redWins = 0

        if self._options.showDisplay:
            self._graphics = HexGraphics()

        self._bluePathFinder = PathBoy(
            self._gameBoard,
            self._gameBoard.getAdjacentSpaces,
            HexGameRules.checkIfBarrier(1,useEmpty=False),
        )
        self._redPathFinder = PathBoy(
            self._gameBoard,
            self._gameBoard.getAdjacentSpaces,
            HexGameRules.checkIfBarrier(2,useEmpty=False),
        )

        self._blueAgent = None
        self._redAgent = None
        self._blueName = ""
        self._redName = ""
        # Set AIs if provided
        if agent1 != None:
            self._blueAgent = agent1
            self._blueName = self._blueAgent.name
            self._blueAgent.setGameBoardAndPlayer(self._gameBoard, 1)

        if agent2 != None:
            self._redAgent = agent2
            self._redName = self._redAgent.name
            self._redAgent.setGameBoardAndPlayer(self._gameBoard, 2)

    '''---
    Game Loops
    ---'''
    def _gameEventLoop(self):
        """Main event Game Loop (Game in progress)"""
        for event in pygame.event.get():
            # Quit button
            if event.type == QUIT:
                self._terminateGame()

            # Mouse click
            elif event.type == MOUSEBUTTONDOWN:
                self._handleMouseClick(pygame.mouse.get_pos())

            # Start Turn
            elif event.type == BEFORE_TURN:
                self._handleAgentTurn()

            # Handle Next move
            elif event.type == PLAYER_TURN:
                self._handleNextMove(self._currentPlayer, self._nextMove)

            # End Turn
            elif event.type == AFTER_TURN:
                self._endTurn()

    def _endGameEventLoop(self):
        """Event loop after a game has been completed"""
        # loop through events.
        for event in pygame.event.get():
            # quit
            if event.type == QUIT:
                self._terminateGame()

    '''---
    Events and handlers
    ---'''
    def _eventStartTurn(self):
        """Trigger Game Event Start Turn"""
        pygame.event.post(pygame.event.Event(BEFORE_TURN))

    def _eventDoPlayerMove(self):
        """Trigger Game Event Player Turn"""
        pygame.event.post(pygame.event.Event(PLAYER_TURN))

    def _eventAfterTurn(self):
        """Trigger Game Event End Turn"""
        pygame.event.post(pygame.event.Event(AFTER_TURN))

    def _handleMouseClick(self, mousePos: Hex):
        """Handle a click on the Game Board"""
        if self._options.showDisplay:
            move = self._graphics.findHexagonCoordsForMousePos(mousePos)
            if self._validatePlayer() and self._gameBoard.validateMove(move):
                self._nextMove = move
                self._eventDoPlayerMove()

    def _handleAgentTurn(self):
        """Handle getting a move from an agent if needed"""
        if self._currentPlayer == 1 and self._blueAgent != None:
            self._nextMove = self._blueAgent.getAgentMove()
            self._eventDoPlayerMove()
        if self._currentPlayer == 2 and self._redAgent != None:
            self._nextMove = self._redAgent.getAgentMove()
            self._eventDoPlayerMove()

    def _handleNextMove(self, player: int, move: Hex):
        """Handle the next move"""
        if self._gameBoard.validateMove(move):
            self._gameBoard.makeMove(move, player)
            self._updateAgentBoards()
            self._eventAfterTurn()

    '''---
    Game Management
    ---'''
    def _endTurn(self):
        """Check the board for a winner or switch turns"""
        if self._currentPlayer == 1:
            # blue just went, Look for a completed blue path
            winPath = self._bluePathFinder.findPath(
                HexGameRules.blue.start,
                HexGameRules.blue.end,
            )

        else:
            # red just went, Look for a completed red path
            winPath = self._redPathFinder.findPath(
                HexGameRules.red.start,
                HexGameRules.red.end,
            )

        # Is the game over?
        if len(winPath) != 0:
            self._winPath = winPath
            self._gameInProgress = False

            if self._blueAgent != None:
                self._blueAgent.scoreGame()
            if self._redAgent != None:
                self._redAgent.scoreGame()

        else:  # switch turns
            self._switchTurns()
            self._eventStartTurn()

    def _validatePlayer(self):
        """Validate if the current player is a human"""
        if self._currentPlayer == 1:
            return self._blueAgent == None
        else:
            return self._redAgent == None

    def _preGameSetup(self): 
        """Setup board and graphics, trigger start turn event"""
        if self._options.showDisplay:
            self._graphics.setupWindow()

        self._gameBoard.resetGameBoard()
        if self._blueAgent != None:
            self._blueAgent.startGame()
        if self._redAgent != None:
            self._redAgent.startGame()

        self._winPath = None
        self._eventStartTurn()

    def _updateGameWindow(self):
        """Update Graphics"""
        if self._options.showDisplay:
            self._graphics.updateWindow(self._gameBoard, self._winPath)

    def _updateAgentBoards(self):
        """Update Agents Boards because it changed"""
        if self._blueAgent != None:
            self._blueAgent.updateBoard()
        if self._redAgent != None:
            self._redAgent.updateBoard()

    def _terminateGame(self):
        """Force Quit game"""
        self._gameInProgress = False
        self._forceQuit = True

    def _playGame(self):
        """Play a game"""
        # Pre Game
        self._preGameSetup()

        # Game
        while self._gameInProgress:
            self._updateGameWindow()
            self._gameEventLoop()

        # Post Game
        self._updateGameWindow()
        if self._currentPlayer == 1:
            self._blueWins += 1
        else:
            self._redWins += 1

        self._gameInProgress = True
        while self._gameInProgress and self._options.showDisplay and self._options.showEndGame:
            self._endGameEventLoop()
            self._updateGameWindow()

    def _switchTurns(self):
        """Switch between blue and red turns"""
        if self._currentPlayer == 1:
            self._currentPlayer = 2
        else:
            self._currentPlayer = 1

    def _printGameSummary(self):
        """Print the current game number and current win summary"""
        if not self._options.showPrint:
            return

        # Note: _currentGameNumber is always one game ahead of the games completed. Showing that the game that is currently being played is the current game. 
        sys.stdout.write(
            "\rGame #%d, Blue%s wins: %d, Red%s wins: %d"
            % (
                self._currentGameNumber,
                self._blueName,
                self._blueWins,
                self._redName,
                self._redWins,
            )
        )
        sys.stdout.flush()

    def _printPostGameSummary(self):
        """Print the Post game summary of win percents"""
        self._currentGameNumber -= 1  # _currentGameNumber is always one game ahead of completed games
        if not self._options.showPrint:
            return

        numGames = self._currentGameNumber
        if numGames == 0: # Always check if divide by zero
            numGames = 1
        blueWinPercent = self._blueWins / numGames
        redWinPercent = self._redWins / numGames
        self._printGameSummary()
        print()
        print("Blue%s Win:  %0.2f" % (self._blueName, blueWinPercent))
        print("Red%s Win:  %0.2f" % (self._redName, redWinPercent))

    '''---
    public
    ---'''
    def main(self, numGames=1):
        """Play a number of hex games"""
        self._printGameSummary()

        for i in range(numGames):
            if not self._forceQuit:
                if (self._options.alternateStartingPlayer):
                    self._currentPlayer = (i % 2) + 1  # alternate starting 
                self._playGame()
                self._currentGameNumber += 1
                self._printGameSummary()

        # Post summary
        self._printPostGameSummary()

'''----------------------------------
Main
----------------------------------'''
def Hex_Play(
    agentA=None,
    agentB=None,
    showEndGame=False,
    showDisplay=True,
    numGames=None,
    showPrint=True,
):
    """Main HexGame Function to play games given config"""

    options = HexGameOptions(
        showDisplay=showDisplay,
        showPrint=showPrint,
        showEndGame=showEndGame
    )

    game = HexGame(
        agent1=agentA,
        agent2=agentB,
        options=options
    )

    game.main(numGames)
