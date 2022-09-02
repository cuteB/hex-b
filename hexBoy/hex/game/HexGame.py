# I don't like the pygame startup message.
from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import random # TODO delete
import sys
from dataclasses import dataclass
from pygame.locals import *
from math import cos, sin, pi # TODO delete?
from typing import List

from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.node.HexNode import HexNode
from hexBoy.hex.HexGraphics import Graphics
from hexBoy.hex.board.HexBoard import Board
from hexBoy.AI.HexAgent import HexAgent

# Custom Events
BEFORE_TURN = pygame.USEREVENT + 1
PLAYER_TURN = pygame.USEREVENT + 2
AFTER_TURN = pygame.USEREVENT + 3

"""----------------------------------
Main hex game class
----------------------------------"""


@dataclass
class HexGame:
    boardSize: int
    hexSize: int

    gameInProgress: bool  # Bool, While true loop through the game
    forceQuit: bool  # bool, force quit the game
    showEndGame: bool
    showDisplay: bool
    showPrint: bool

    player: int  # Int, Current player. Blue=1, Red=2
    winPath: List[tuple]  # (x,y)[], list of coordinates for the winning path

    graphics: Graphics  # Graphics, render the game board
    board: Board  # Board, Hex Board Object
    bluePathFinder: PathBoy  # Pathfinder, Algorithms to find paths
    redPathfinder: PathBoy

    gameNumber: int
    blueAgent: HexAgent  # AIs for player, None = human
    redAgent: HexAgent
    blueWins: int
    redWins: int
    blueName: str
    redName: str

    nextMove: tuple

    def __init__(
        self,
        computer1=None,
        computer2=None,
        showDisplay=False,
        showEndGame=False,
        showPrint=False,
    ):
        pygame.init()

        self.boardSize = 11
        self.hexSize = 40 # TODO move to HexGraphics
        self.gameInProgress = True  # game loop check
        self.forceQuit = False
        self.player = 1  # current player's turn, Blue starts #TODO rename playerTurn

        self.showDisplay = showDisplay  # somtimes hide the display

        self.winPath = None
        # TODO move the game options in the same block
        self.showEndGame = showEndGame
        self.showPrint = showPrint

        if self.showDisplay:
            self.graphics = Graphics(self.boardSize, self.hexSize)
        self.board = Board(self.boardSize)


        self.bluePathFinder = PathBoy(
            self.board,
            self.board.getAdjacentSpaces,
            HexNode.checkIfBlueBarrier,
        )
        self.redPathFinder = PathBoy(
            self.board,
            self.board.getAdjacentSpaces,
            HexNode.checkIfRedBarrier,
        )

        # TODO move all of the one line declarations to the start
        self.gameNumber = 1
        self.blueWins = 0
        self.redWins = 0
        self.blueAgent = None
        self.redAgent = None
        self.blueName = ""
        self.redName = ""
        # Set AIs if provided
        if computer1 != None:
            self.blueAgent = computer1
            self.blueName = self.blueAgent.name
            self.blueAgent.setGameBoardAndPlayer(self.board, 1)

        if computer2 != None:
            self.redAgent = computer2
            self.redName = self.redAgent.name
            self.redAgent.setGameBoardAndPlayer(self.board, 2)

    '''---
    Game Loops
    ---'''
    def gameEventLoop(self):
        """Main event Game Loop (Game in progress)"""
        for event in pygame.event.get():
            # Quit button
            if event.type == QUIT:
                self.terminateGame()

            # Mouse click
            elif event.type == MOUSEBUTTONDOWN:
                self.handleMouseClick(pygame.mouse.get_pos())

            # Start Turn
            elif event.type == BEFORE_TURN:
                self.handleAgentTurn()

            # Handle Next move
            elif event.type == PLAYER_TURN:
                self.handleNextMove(self.nextMove, self.player)

            # End Turn
            elif event.type == AFTER_TURN:
                self.endTurn()

    def endGameEventLoop(self):
        """Event loop after a game has been completed"""
        # loop through events.
        for event in pygame.event.get():
            # quit
            if event.type == QUIT:
                self.terminateGame()

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

    def handleMouseClick(self, mousePos):
        """Handle a click on the Game Board"""
        if self.showDisplay:
            move = self.graphics.findHexagonCoordsForMousePos(mousePos)
            if self.validatePlayer() and self.board.validateMove(move):
                self.nextMove = move
                self._eventDoPlayerMove()

    def handleAgentTurn(self):
        """Handle getting a move from an agent if needed"""
        if self.player == 1 and self.blueAgent != None:
            self.nextMove = self.blueAgent.getAgentMove()
            self._eventDoPlayerMove()
        if self.player == 2 and self.redAgent != None:
            self.nextMove = self.redAgent.getAgentMove()
            self._eventDoPlayerMove()

    def handleNextMove(self, move, player):
        """Handle the next move"""
        if self.board.validateMove(move):
            self.board.makeMove(move, player)
            self._updateAgentBoards()
            self._eventAfterTurn()

    '''---
    Game Mangement
    ---'''

    def endTurn(self):
        """Check the board for a winner or switch turns"""
        if self.player == 1:
            # blue just went, Look for a completed blue path
            winPath = self.bluePathFinder.findPath(
                self.board.blueStartSpace,
                self.board.blueEndSpace,
            )

        else:
            # red just went, Look for a completed red path
            winPath = self.redPathFinder.findPath(
                self.board.redStartSpace,
                self.board.redEndSpace,
            )

        # Is the game over?
        if len(winPath) != 0:
            self.winPath = winPath
            self.gameInProgress = False

            if self.blueAgent != None:
                self.blueAgent.scoreGame()
            if self.redAgent != None:
                self.redAgent.scoreGame()

        else:  # switch turns
            self._switchTurns()
            self._eventStartTurn()

    def validatePlayer(self):
        """Validate if the current player is a human"""
        if self.player == 1:
            return self.blueAgent == None
        else:
            return self.redAgent == None

    def _setup(self): # TODO rename, what is it setting up?
        """Setup board and graphics, trigger start turn event"""
        if self.showDisplay:
            self.graphics.setupWindow()

        self.board.resetGame()
        if self.blueAgent != None:
            self.blueAgent.startGame()
        if self.redAgent != None:
            self.redAgent.startGame()

        self.winPath = None
        self._eventStartTurn()

    # Update display
    def updateGame(self): # TODO rename updateGameWindow
        """Update Graphics"""
        if self.showDisplay:
            self.graphics.updateWindow(self.board, self.winPath)

    def _updateAgentBoards(self): # TODO figure out the _ prefix, so random
        """Update Agents Boards because it changed"""
        if self.blueAgent != None:
            self.blueAgent.updateBoard()
        if self.redAgent != None:
            self.redAgent.updateBoard()

    def terminateGame(self):
        """Force Quit game"""
        self.gameInProgress = False
        self.forceQuit = True

    def playGame(self):
        """Play a game"""
        # Pre Game
        self._setup()
        # Game
        while self.gameInProgress:
            self.updateGame()
            self.gameEventLoop()

        # Post Game
        self.updateGame()
        if self.player == 1:
            self.blueWins += 1
        else:
            self.redWins += 1

        self.gameInProgress = True
        while self.gameInProgress and self.showDisplay and self.showEndGame:
            self.endGameEventLoop()
            self.updateGame()

    def _switchTurns(self):
        """Switch between blue and red turns"""
        # TODO have the option to not switch turns
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1
            # return True # tf is this 

    # Return the position of the clicked cell in the board matrix
    def onClickFindHexagonCoords(self): # TODO delete, already in HexGraphics
        # Just going to half ass this on click for now. Want it to work before
        # getting the perfect hex click function. (Half ass algorithm works well)
        #
        # Right now I'll basically create a grid to get a rough estimate
        # of what cell was clicked. Will work fine when the user clicks in the middle
        #
        # Using Rectangles to estimate the hexagon
        # - Height = Hexagon Size
        # - Width = Hexagon Size * 3/4 (Need to account for interlock)
        """
         __
        |  |__
        |__|  |__
        |  |__|  |
        |__|  |__|
        |  |__|  |
        |__|  |__|
           |__|  |
              |__|
        """

        (xMouse, yMouse) = self.mousePos
        hexSize = self.hexSize

        # Extra space between screen border and hexagons
        borderOffset = (hexSize / 2) + (hexSize / 8)
        rectWidth = hexSize * (3 / 4)  # using rectangles to estimate the hexagons
        rectHeight = hexSize

        # adjust for left border and divide by the rectangle width to get x value
        xMouseAdjusted = xMouse - borderOffset
        xRow = xMouseAdjusted // rectWidth

    def _printGameSummary(self):
        """Print the current game number and current win summary"""
        if not self.showPrint:
            return
        sys.stdout.write(
            "\rGame #%d, Blue%s wins: %d, Red%s wins: %d"
            % (
                self.gameNumber,
                self.blueName,
                self.blueWins,
                self.redName,
                self.redWins,
            )
        )
        sys.stdout.flush()

    def _printPostGameSummary(self):
        """Print the Post game summary of win percents"""
        self.gameNumber -= 1  # always one game ahead
        if not self.showPrint:
            return

        numGames = self.gameNumber
        if numGames == 0:
            numGames = 1
        blueWinPerc = self.blueWins / numGames
        redWinPerc = self.redWins / numGames
        self._printGameSummary()
        print()
        print("Blue%s Win:  %0.2f" % (self.blueName, blueWinPerc))
        print("Red%s Win:  %0.2f" % (self.redName, redWinPerc))

    """---
    Main Hex Game
    ---"""
    def main(self, numGames=1):
        """Play a number of hex games"""
        self._printGameSummary()

        for i in range(numGames):
            if not self.forceQuit:
                self.player = (i % 2) + 1  # altertate turns
                self.playGame()
                self.gameNumber += 1
                self._printGameSummary()

        # Post summary
        self._printPostGameSummary()


"""----------------------------------
Main
----------------------------------"""


def Hex_Play(
    agentA=None,
    agentB=None,
    showEndGame=False,
    showDisplay=True,
    numGames=None,
    showPrint=True,
):
    """Main HexGame Function to play games given config"""
    game = HexGame(
        computer1=agentA,
        computer2=agentB,
        showEndGame=showEndGame,
        showDisplay=showDisplay,
        showPrint=showPrint,
    )

    game.main(numGames)
