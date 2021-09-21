# I don't like the pygame startup message. Needs to be before pygame import
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import random
import sys
from pygame.locals import *
from math import cos, sin, pi

# My imports
from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.HexNode import HexNode
from hexBoy.hex.HexGraphics import Graphics
from hexBoy.hex.HexBoard import Board

# Custom Events
DO_MOVE = pygame.USEREVENT + 1
'''
-----------------------------------------------
Main hex game class
-----------------------------------------------
'''
class HexGame:
  hexSize     = None  # Int, Size of the hexagons in pixels
  boardSize   = None  # Int, Size of the playing board (default is 11)

  playing     = None  # Bool, While true loop through the game
  quitGame    = None  # bool, force quit the game
  turn        = None  # Int, Current player. Blue=1, Red=2
  winPath     = None  # (x,y)[], list of coordinates for the winning path
  showOutput  = None  # show print statements

  graphics    = None  # Graphics, render the game board
  board       = None  # Board, Hex Board Object
  pathfinder  = None  # Pathfinder, Algorithms to find paths

  blueAgent   = None  # AIs for player, None = human
  redAgent    = None

  nextMove = None

  def __init__(self,
    computer1 = None,
    computer2 = None,
    showDisplay = True,
    showEndGame = True
  ):
    pygame.init()

    self.showDisplay = showDisplay # somtimes hide the display
    self.hexSize = 40
    self.boardSize = 11

    self.playing = True # game loop check
    self.quitGame = False
    self.turn = 1       # current player's turn, Blue starts
    self.winPath = None
    self.showEndGame = showEndGame
    self.showOutput = True

    if (self.showDisplay):
      self.graphics = Graphics(self.boardSize, self.hexSize)

    self.board = Board(self.boardSize)
    self.pathfinder = PathBoy(self.board.getAdjacentSpaces, 0)

    # Set AIs if provided
    if (computer1 != None):
      self.blueAgent = computer1
      self.blueAgent.setGameBoardAndPlayer(self.board, 1)

    if (computer2 != None):
      self.redAgent = computer2
      self.redAgent.setGameBoardAndPlayer(self.board, 2)


  '''
  ------------------
  Game Loops
  ------------------
  '''
  # event loop when the game is being played
  def eventLoop(self):
    # loop through events
    for event in pygame.event.get():

      # Quit button
      if event.type == QUIT:
        self.terminateGame()

      # Mouse click
      if (event.type == MOUSEBUTTONDOWN):
        self.mousePos = pygame.mouse.get_pos()
        # Grab the cell coords that the click was in
        cell = self.onClickFindHexagonCoords()
        # Check if the click was in a cell on the board
        if self.validateClickCell(cell):
          # Check if it is a valid move and do the move
          if (self.validatePlayer() and self.board.validateMove(cell)):
            self.board.makeMove(cell, self.turn)
            self.endTurn()

      elif (event.type == DO_MOVE):
        cell = self.nextMove
        if (self.board.validateMove(cell)):
          self.board.makeMove(cell, self.turn)
          self.endTurn()

  # event loop after the game is finished
  def endEventLoop(self):
    # loop through events
    for event in pygame.event.get():

      # quit
      if event.type == QUIT:
        self.terminateGame()

  '''
  ------------------
  Game Management
  ------------------
  '''
  # TODO agent needs to score game after updating the window. Currently doesn't show the last move on the board

  def startTurn(self):
    self.updateGame()
    # not much happens at the start of the turn

    # if the current player is an AI get it's move

    if (self.turn == 1 and self.blueAgent != None):
      self.nextMove = self.blueAgent.getAgentMove()
      pygame.event.post(pygame.event.Event(DO_MOVE))

    elif (self.turn == 2 and self.redAgent != None):
      self.nextMove = self.redAgent.getAgentMove()
      pygame.event.post(pygame.event.Event(DO_MOVE))

  # End of turn process. Evaluate position.
  # Check if there is a winner or go to next player's turn
  def endTurn(self):
    # Blue=1, Red=2
    if (self.turn == 1):
      # blue just went, Look for a completed blue path
      winPath = self.pathfinder.findPath(
        self.board.getNodeDict(),
        self.board.blueStartSpace,
        self.board.blueEndSpace,
        HexNode.checkIfBlueBarrier,
        HexNode.getCellValueForWinningPath
      )

      # found a winning path for blue
      if (len(winPath) != 0):
        if (self.showOutput):
          print("Blue Wins!")

        self.winPath = winPath
        self.playing = False

        self.updateGame()
        if (self.blueAgent != None):
          self.blueAgent.scoreGame()
        if (self.redAgent != None):
          self.redAgent.scoreGame()

      else: # go to red's turn
        self.turn = 2;
        self.startTurn()

    else:
      # red just went, Look for a completed red path
      winPath = self.pathfinder.findPath(
        self.board.getNodeDict(),
        self.board.redStartSpace,
        self.board.redEndSpace,
        HexNode.checkIfRedBarrier,
        HexNode.getCellValueForWinningPath
      )

      # found a winning path for red
      if (len(winPath) != 0):
        if (self.showOutput):
          print("Red Wins!")

        self.winPath = winPath
        self.playing = False

        self.updateGame()
        if (self.redAgent != None):
          self.redAgent.scoreGame()
        if (self.blueAgent != None):
          self.blueAgent.scoreGame()

      else: # go to Blue's turn
        self.turn = 1
        self.startTurn()

  # Check if the current turn is for an AI
  # don't let the human player make the move if its the computer's turn
  def validatePlayer(self):
    turn = self.turn

    if (turn == 1):
      return self.blueAgent == None
    else:
      return self.redAgent == None

  # Setup game and start first turn
  def setupGame(self):

    if self.showDisplay:
      self.graphics.setupWindow()

    self.board.resetGame()

    self.winPath = None

    self.startTurn()

  # Update display
  def updateGame(self):
    if self.showDisplay:
      self.graphics.updateWindow(self.board, self.winPath)

  # Exit the game
  def terminateGame(self):
    self.playing = False
    self.quitGame = True

  def playGame(self):
    self.setupGame()

    # main game loop
    while (self.playing):
      self.eventLoop()
      self.updateGame()

    # end game loop
    self.playing = True
    while (self.playing and self.showDisplay and self.showEndGame):
      self.endEventLoop()
      self.updateGame()

    return self.turn

  '''
  ------------------
  Handle clicks on the board
  ------------------
  '''
  # Check if the click was on a valid cell
  def validateClickCell(self, cellCoords):
    (row, col) = cellCoords

    if (row < 0 or col < 0):
      return False
    elif (row >= self.boardSize or col >= self.boardSize):
      return False
    else:
      return True

  # Return the position of the clicked cell in the board matrix
  def onClickFindHexagonCoords(self):
    # Just going to half ass this on click for now. Want it to work before
    # getting the perfect hex click function. (Half ass algorithm works well)
    #
    # Right now I'll basically create a grid to get a rough estimate
    # of what cell was clicked. Will work fine when the user clicks in the middle
    #
    # Using Rectangles to estimate the hexagon
    # - Height = Hexagon Size
    # - Width = Hexagon Size * 3/4 (Need to account for interlock)
    '''
     __
    |  |__
    |__|  |__
    |  |__|  |
    |__|  |__|
    |  |__|  |
    |__|  |__|
       |__|  |
          |__|
    '''

    (xMouse, yMouse) = self.mousePos
    hexSize = self.hexSize

    # Extra space between screen border and hexagons
    borderOffset = (hexSize / 2) + (hexSize / 8)
    rectWidth = hexSize * (3/4) # using rectangles to estimate the hexagons
    rectHeight = hexSize

    # adjust for left border and divide by the rectangle width to get x value
    xMouseAdjusted = xMouse - borderOffset
    xRow = xMouseAdjusted // rectWidth

    # adjust for top border
    # account for offset y coords of columns as rows increase
    # divide by rectangle height to get y value
    yMouseAdjusted = (yMouse - borderOffset)
    yMouseAdjusted -= (xRow * rectHeight / 2)
    yRow = yMouseAdjusted // rectHeight

    # make sure type int
    return (int(xRow), int(yRow))

  '''
  ------------------
  Main Hex Game
  ------------------
  '''
  def main(self, numGames = None):

    if (numGames == None):
      self.playGame()

    else:
      self.showOutput = False

      blueWins = 0
      redWins = 0
      blueName = ""
      redName = ""

      if (self.blueAgent != None):
        blueName = self.blueAgent.name

      if (self.redAgent != None):
        redName = self.redAgent.name

      for i in range(numGames):
        if (not self.quitGame):
          self.turn = (i % 2) + 1 # altertate turns
          self.playGame()

          if (self.turn == 1):
            blueWins += 1
          else:
            redWins += 1

        sys.stdout.write("\rGame #%d, Blue%s wins: %d, Red%s wins: %d" % (i+1, blueName, blueWins, redName, redWins))
        sys.stdout.flush()

      numGames = blueWins + redWins
      blueWinPerc = blueWins / numGames
      redWinPerc = redWins / numGames
      print()
      print("Blue%s Win:  %0.2f" % (blueName, blueWinPerc))
      print("Red%s Win:  %0.2f" % (redName, redWinPerc))

'''
-----------------------------------------------
Main
-----------------------------------------------
'''
def HexGame_Play(
  agentA = None,
  agentB = None,
  showEndGame = False,
  showDisplay = True,
  numGames = None
):

  # game = HexGame()
  game = HexGame(
    computer1=agentA,
    computer2=agentB,
    showEndGame = showEndGame,
    showDisplay = showDisplay,
  )

  game.main(numGames)
