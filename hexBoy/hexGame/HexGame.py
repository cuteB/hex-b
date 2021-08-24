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

  def __init__(self):
    pygame.init()

    self.hexSize = 40
    self.boardSize = 11

    self.playing = True # game loop check
    self.turn = 1       # current player's turn, Blue starts
    self.winPath = None

    self.graphics = Graphics(self.boardSize, self.hexSize)
    self.board = Board(self.boardSize)
    self.pathfinder = Pathfinder(self.board.getAdjacentSpaces, 0)

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

  # Setup game
  def setupGame(self):
    self.graphics.setupWindow()

  # Update display
  def updateGame(self):
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
    while self.playing:
      self.eventLoop()
      self.updateGame()

    # end game loop
    self.playing = True
    while self.playing:
      self.endEventLoop()
      self.updateGame()

'''
-----------------------------------------------
Game Board
-----------------------------------------------
'''
class Board:
  boardDict       = None  # dict<HexNode>, Cells on the board and their values
  boardSize       = None  # int, size of the board

  # HexNode.Space, object of the different types of hex spaces.
  hexTypes      = None

  # tuples of the (x,y) coordinates of the red/blue start/end spaces
  redStartSpace   = None
  redEndSpace     = None
  blueStartSpace  = None
  blueEndSpace    = None

  def __init__(self, boardSize):
    self.boardSize = boardSize
    self.hexTypes = HexNode.Space

    self.redStartSpace = (-1, 0)
    self.redEndSpace = (self.boardSize, self.boardSize - 1)
    self.blueStartSpace = (0, -1)
    self.blueEndSpace = (self.boardSize -1, self.boardSize)

    self.boardDict = self.initGameBoard()

  # Return the board node dict
  def getNodeDict(self):
    return self.boardDict

  # Initialize the starting game board.
  def initGameBoard(self):
    dict = {}

    #initialize playing spaces
    for x in range(self.boardSize):
      for y in range(self.boardSize):
        dict[(x,y)] = HexNode(self.hexTypes.EMPTY)

    # Itialize edges in dict
    # blue edge
    for x in range(self.boardSize):
      dict[(x,-1)] = HexNode(self.hexTypes.BLUE_EDGE)
      dict[(x,self.boardSize)] = HexNode(self.hexTypes.BLUE_EDGE)
    # red edge
    for y in range(self.boardSize):
      dict[(-1,y)] = HexNode(self.hexTypes.RED_EDGE)
      dict[(self.boardSize,y)] = HexNode(self.hexTypes.RED_EDGE)

    return dict

  # Check if the given cell is a valid move. (hex is empty)
  def validateMove(self, cell):
    return self.boardDict[cell].getValue() == self.hexTypes.EMPTY

  # Make the move on the board dict
  def makeMove(self, cell, player):
    self.boardDict[cell].setValue(player)

  # Check if the move is within the board or edges
  def isSpaceWithinBounds(self, cell):
    boardSize = self.boardSize
    x = cell[0]
    y = cell[1]

    # include the edges around the matrix, cells within [-1, boardsize] bound.
    return (x >= -1 and y >= -1
      and x <= boardSize and y <= boardSize
      # Don't include (-1,-1), (-1, len), (len, -1), (len, len)
      and not ((x == -1 or x == boardSize) and (y == -1 or y == boardSize)))

  # Get adjacent spaces
  def getAdjacentSpaces(self, cell):
    '''
    Here is what the hex space looks like. just treat them like squares
    with too extra edges
     ___
    /0,0\___
    \___/1,0\___
    /0,1\___/2,0\___
    \___/1,1\___/3,0\
    /0,2\___/2,1\___/
    \___/1,2\___/3,1\
    /0,3\___/2,2\___/
    \___/1,3\___/3,2\
        \___/2,3\___/
            \___/3,3\
                \___/
    '''
    x = cell[0]
    y = cell[1]

    # eg for cell       (1,1)
    adjacentSpaces = []
    potentialSpaces = [
      (x,   y-1),     # (1,0) up
      (x,   y+1),     # (1,2) down
      (x-1, y),       # (0,1) left
      (x+1, y),       # (2,1) right
      (x-1, y+1),     # (0,2) down+left
      (x+1, y-1),     # (2,0) up+right
    ]

    # validate the potential spaces and return the adjacent spaces
    for space in potentialSpaces:
      if (self.isSpaceWithinBounds(space)):
        adjacentSpaces.append(space)

    return adjacentSpaces

'''
-----------------------------------------------
Main
-----------------------------------------------
'''
def HexGame_main():
  game = HexGame()
  game.main()
