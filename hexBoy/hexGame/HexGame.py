# I don't like the pygame startup message. Needs to be before pygame import
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
from pygame.locals import *
from math import cos, sin, pi

# My imports
from hexGame.Pathfinder import Pathfinder
from hexGame.HexNode import HexNode
from hexGame.HexGraphics import Graphics
from hexGame.HexBoard import Board
from hexGame.HexAI import HexAI

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
  turn        = None  # Int, Current player. Blue=1, Red=2
  winPath     = None  # (x,y)[], list of coordinates for the winning path

  graphics    = None  # Graphics, render the game board
  board       = None  # Board, Hex Board Object
  pathfinder  = None  # Pathfinder, Algorithms to find paths

  player1AI   = None  # AIs for player, None = human
  player2AI   = None

  nextMove = None

  def __init__(self, computer1 = None, computer2 = None, showDisplay = True):
    pygame.init()

    self.showDisplay = showDisplay # somtimes hide the display
    self.hexSize = 40
    self.boardSize = 11

    self.playing = True # game loop check
    self.turn = 1       # current player's turn, Blue starts
    self.winPath = None

    if (self.showDisplay):
      self.graphics = Graphics(self.boardSize, self.hexSize)

    self.board = Board(self.boardSize)
    self.pathfinder = Pathfinder(self.board.getAdjacentSpaces, 0)

    # Set AIs if provided
    if (computer1 != None):
      self.player1AI = computer1

    if (computer2 != None):
      self.player2AI = computer2

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

      if (event.type == DO_MOVE):
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
  def startTurn(self):
    # not much happens at the start of the turn

    # if the current player is an AI get it's move

    if (self.turn == 1 and self.player1AI != None):
      self.nextMove = self.player1AI.makeMove(self.board)
      pygame.event.post(pygame.event.Event(DO_MOVE))

    elif (self.turn == 2 and self.player2AI != None):
      self.nextMove = self.player2AI.makeMove(self.board)
      pygame.event.post(pygame.event.Event(DO_MOVE))

  # End of turn process. Evaluate position.
  # Check if there is a winner or go to next player's turn
  def endTurn(self):
    # Blue=1, Red=2
    if (self.turn == 1):
      # blue just went, Look for a completed blue path
      winPath = self.pathfinder.AStar(
        self.board.getNodeDict(),
        self.board.blueStartSpace,
        self.board.blueEndSpace,
        HexNode.checkIfBlueBarrier
      )

      # found a winning path for blue
      if (len(winPath) != 0):
        print("Blue Wins!")
        self.winPath = winPath
        self.playing = False

      else: # go to red's turn
        self.turn = 2;
        self.startTurn()

    else:
      # red just went, Look for a completed red path
      winPath = self.pathfinder.AStar(
        self.board.getNodeDict(),
        self.board.redStartSpace,
        self.board.redEndSpace,
        HexNode.checkIfRedBarrier
      )

      # found a winning path for red
      if (len(winPath) != 0):
        print("Red Wins!")
        self.winPath = winPath
        self.playing = False

      else: # go to Blue's turn
        self.turn = 1
        self.startTurn()

  # Check if the current turn is for an AI
  # don't let the human player make the move if its the computer's turn
  def validatePlayer(self):
    turn = self.turn

    if (turn == 1):
      return self.player1AI == None
    else:
      return self.player2AI == None

  # Setup game
  def setupGame(self):
    if self.showDisplay:
      self.graphics.setupWindow()

  # Update display
  def updateGame(self):
    if self.showDisplay:
      self.graphics.updateWindow(self.board, self.winPath)

  # Exit the game
  def terminateGame(self):
    self.playing = False

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
  def main(self):
    self.setupGame()

    # main game loop
    self.startTurn()
    while (self.playing):
      self.eventLoop()
      self.updateGame()

    # end game loop
    self.playing = True
    while (self.playing and self.showDisplay):
      self.endEventLoop()
      self.updateGame()

'''
-----------------------------------------------
Main
-----------------------------------------------
'''
def HexGame_main():
  hexBoy = HexAI()

  # game = HexGame()
  game = HexGame(computer1 = hexBoy, computer2 = hexBoy)
  game.main()
