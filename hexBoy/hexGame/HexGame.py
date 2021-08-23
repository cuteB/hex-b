# I don't like the pygame startup message so I hide. Also doesn't work
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import sys
from pygame.locals import *
from math import cos, sin, pi

from hexGame.Pathfinder import Pathfinder
from hexGame.HexNode import HexNode

# COLOURS  R    G    B
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)
DARK_RED = (150, 0, 0)
DARK_BLUE = (0,0,150)

'''
-----------------------------------------------
Main hex game class
-----------------------------------------------
'''
class HexGame:
  def __init__(self):
    pygame.init()

    self.hexSize = 40
    self.boardSize = 11

    self.playing = True # game loop check
    self.turn = 1    # current player's turn (1 = blue, 2 = red)
    self.graphics = Graphics(self.boardSize, self.hexSize)
    self.board = Board(self.boardSize)
    self.pathfinder = Pathfinder(self.board.getAdjacentSpaces, 0)
    self.winPath = None

  def setupGame(self):
    self.graphics.setupWindow()

  '''
  Main Event loop
  Check events and do the things
  '''
  def eventLoop(self):
    self.mousePos = pygame.mouse.get_pos()

    # loop through events
    for event in pygame.event.get():
      # get mouse position

      # quit
      if event.type == QUIT:
        self.terminateGame()

      # Mouse click
      if (event.type == MOUSEBUTTONDOWN):
        cell = self.onClickFindHexagonCoords()
        # Check if the click was in a cell on the board
        if self.validateClickCell(cell):
          # Check if it is a valid move and do the move if it is
          if (self.board.validateMove(cell)):
            self.board.makeMove(cell, self.turn)
            self.endTurn()

  def endEventLoop(self):
    # loop through events
    for event in pygame.event.get():
      # get mouse position

      # quit
      if event.type == QUIT:
        self.terminateGame()

  # Swap player turns
  def endTurn(self):
    if (self.turn == 1):
      # blue just went
      winPath = self.pathfinder.AStar(
        self.board.getNodeDict(),
        self.board.blueStartSpace,
        self.board.blueEndSpace,
        HexNode.checkIfBlueBarrier
      )


      if (len(winPath) != 0):
        print("Blue Wins!")
        self.winPath = winPath
        self.playing = False
      else:
        self.turn = 2; # red's turn next
    else:
      # red just went
      winPath = self.pathfinder.AStar(
        self.board.getNodeDict(),
        self.board.redStartSpace,
        self.board.redEndSpace,
        HexNode.checkIfRedBarrier
      )

      if (len(winPath) != 0):
        print("Red Wins!")
        self.winPath = winPath
        self.playing = False
      else:
        self.turn = 1 # blue's turn next



  # Update display
  def update(self):
    self.graphics.updateWindow(self.board, self.winPath)

  # Exit the game
  def terminateGame(self):
    self.playing = False

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

    (xMouse, yMouse) = self.mousePos

    hexSize = self.hexSize

    # Extra space between screen border and hexagons
    borderOffset = (hexSize / 2) + (hexSize / 8)
    rectWidth = hexSize * (3/4) # using rectangles to estimate the hexagons
    rectHeight = hexSize

    xMouseAdjusted = xMouse - borderOffset
    xRow = xMouseAdjusted // rectWidth

    #account for offset y coords of columns as rows increase
    yMouseAdjusted = (yMouse - borderOffset)
    yMouseAdjusted -= (xRow * rectHeight / 2)
    yRow = yMouseAdjusted // rectHeight

    return (int(xRow), int(yRow))

  def main(self):
    self.setupGame()

    # main game loop
    while self.playing:
      self.eventLoop()
      self.update()

    # end game loop
    print(self.winPath)
    self.playing = True
    while self.playing:
      self.endEventLoop()
      self.update()


'''
-----------------------------------------------
Game Board
-----------------------------------------------
'''
class Board:
  boardDict = None
  boardSize = None
  SpaceProps = None

  redStartSpace = None
  redEndSpace = None
  blueStartSpace = None
  blueEndSpace = None

  def __init__(self, boardSize):
    self.boardSize = boardSize
    self.boardDict = self.initGameBoard()
    self.spaceProps = HexNode.Space

    self.redStartSpace = (-1, 0)
    self.redEndSpace = (self.boardSize, self.boardSize - 1)
    self.blueStartSpace = (0, -1)
    self.blueEndSpace = (self.boardSize -1, self.boardSize)

  def getNodeDict(self):
    return self.boardDict

  def initGameBoard(self):
    dict = {}
    hexTypes = HexNode.Space

    #initialize playing spaces
    for x in range(self.boardSize):
      for y in range(self.boardSize):
        dict[(x,y)] = HexNode(hexTypes.EMPTY)

    # Itialize edges in dict
    # Initialize blue edge
    for x in range(self.boardSize):
      dict[(x,-1)] = HexNode(hexTypes.BLUE_EDGE)
      dict[(x,self.boardSize)] = HexNode(hexTypes.BLUE_EDGE)
    # Initialize red edge
    for y in range(self.boardSize):
      dict[(-1,y)] = HexNode(hexTypes.RED_EDGE)
      dict[(self.boardSize,y)] = HexNode(hexTypes.RED_EDGE)

    return dict

  def validateMove(self, cell):
    return self.boardDict[cell].getValue() == self.spaceProps.EMPTY

  def makeMove(self, cell, player):
    self.boardDict[cell].setValue(player)

  def isSpaceWithinBounds(self, cell):
    boardSize = self.boardSize
    x = cell[0]
    y = cell[1]

    # include the edges around the matrix, cells within [-1, boardsize] bound
    return x >= -1 and y >= -1 and x <= boardSize and y <= boardSize and not ((x == -1 or x == boardSize) and (y == -1 or y == boardSize))

  def getAdjacentSpaces(self, cell):
    x = cell[0]
    y = cell[1]

    adjacentSpaces = []
    potentialSpaces = [
      (x,   y-1),
      (x,   y+1),
      (x-1, y),
      (x+1, y),
      (x-1, y+1),
      (x+1, y-1),
    ]

    for space in potentialSpaces:
      if (self.isSpaceWithinBounds(space)):
        adjacentSpaces.append(space)

    return adjacentSpaces

'''
-----------------------------------------------
All Graphics drawing hexagons on a board
-----------------------------------------------
'''
# ty https://github.com/ThomasRush/py_a_star for the Hexagon rendering ideas
class Graphics:
  def __init__(self, size, hexSize):
    self.hexSize = hexSize        # Hexagon size in pixels
    self.boardSize = size         # Board size in Hexagons
    self.caption = "Hex Game"

    self.fps = 60
    self.clock = pygame.time.Clock()

    self.xWindowLength = 400
    self.yWindowLength = 700
    self.screen = pygame.display.set_mode(
      (self.xWindowLength, self.yWindowLength)
    )

    self.hexBlue = Hexagon(BLUE, self.hexSize, True)
    self.hexRed = Hexagon(RED, self.hexSize, True)
    self.hexWhite = Hexagon(WHITE, self.hexSize, True)
    self.hexBlueEdge = Hexagon(BLUE, self.hexSize, False)
    self.hexRedEdge = Hexagon(RED, self.hexSize, False)
    self.hexBlack = Hexagon(BLACK, self.hexSize, False)
    self.hexBlueWin =  Hexagon(DARK_BLUE, self.hexSize, True)
    self.hexRedWin =  Hexagon(DARK_RED, self.hexSize, True)

  def setupWindow(self):
    pygame.display.set_caption(self.caption)
    self.screen.fill(WHITE)
    # pygame.draw.rect(self.screen, BLUE, (40, 0, 700, 250))
    # pygame.draw.rect(self.screen, BLUE, (0, 400, 360, 400))

    boardSize = self.boardSize
    hexSize = self.hexSize

    # Draw boarder Hexagons for red and blue sides
    for x in range(boardSize + 2):
      for y in range(boardSize + 2):
        # if it is an edge
        if x == 0 or x == (boardSize + 1) or y == 0 or y == (boardSize + 1):
          xPos = x * hexSize - (hexSize / 4)
          yPos = y * hexSize - (hexSize)

          # offset yPos. Each column is half lower than previous
          yPos += x * (hexSize / 2)
          # offset xPos. Each row is quarter more to the left
          xPos -= x * (hexSize / 4)

        # Render the hex based on board position
        if (x == 0 and y == 0) or (x == (boardSize+1) and y == (boardSize+1)):
          self.screen.blit(self.hexBlack.getHexagon(), (xPos, yPos))
        elif x == 0 or (x == (boardSize + 1)):
          self.screen.blit(self.hexRedEdge.getHexagon(), (xPos, yPos))
        else:
          self.screen.blit(self.hexBlueEdge.getHexagon(), (xPos, yPos))

    pygame.display.flip()

  # Put the hexagons on the board
  def updateWindow(self, gameBoard, winPath = []):

    board = gameBoard.getNodeDict()

    boardSize = self.boardSize
    hexSize = self.hexSize
    borderOffset = hexSize / 2 # Extra space between screen border and hexagons

    # draw hexagons
    for x in range(boardSize):
      for y in range(boardSize):
        cell = (x,y)

        xPos = x * hexSize + borderOffset
        yPos = y * hexSize + borderOffset

        # offset yPos. Each column is half lower than previous
        yPos += x * (hexSize / 2)
        # offset xPos. Each row is quarter more to the left
        xPos -= x * (hexSize / 4)

        # Render the hex based on board position
        if board[cell].getValue() == 1:
          self.screen.blit(self.hexBlue.getHexagon(), (xPos, yPos))
        elif board[cell].getValue() == 2:
          self.screen.blit(self.hexRed.getHexagon(), (xPos, yPos))
        else:
          self.screen.blit(self.hexWhite.getHexagon(), (xPos, yPos))

    # Draw path if supplied
    if (winPath != None and len(winPath) != 0):
      for pos in winPath:
        cell = (pos[0],pos[1])

        xPos = pos[0] * hexSize + borderOffset
        yPos = pos[1] * hexSize + borderOffset

        # offset yPos. Each column is half lower than previous
        yPos += pos[0] * (hexSize / 2)
        # offset xPos. Each row is quarter more to the left
        xPos -= pos[0] * (hexSize / 4)

        if board[cell].getValue() == 1:
          self.screen.blit(self.hexBlueWin.getHexagon(), (xPos, yPos))
        elif board[cell].getValue() == 2:
          self.screen.blit(self.hexRedWin.getHexagon(), (xPos, yPos))

    pygame.display.flip()

    self.clock.tick(self.fps)

'''
-----------------------------------------------
Hexagon shape for board
-----------------------------------------------
'''
class Hexagon:
  def __init__(self, colour, size, drawEdges):
    self.colour = colour
    self.hexSize = size
    self.drawEdges = drawEdges

  def getHexagon(self):
    hexSize = self.hexSize
    surface = pygame.Surface((hexSize, hexSize))

    # fill in background and set it as the transparent colour
    surface.fill(WHITE)
    surface.set_colorkey(WHITE)

    half = hexSize / 2 # half of the hexagon size
    qter = hexSize / 4 # quarter of the hexagon size

    # Hexagon points
    #  1 2
    # 6   3
    #  5 4
    point1 = (qter,        0)
    point2 = (3 * qter,    0)
    point3 = (hexSize - 1, half)
    point4 = (3 * qter,    hexSize - 1)
    point5 = (qter,        hexSize - 1)
    point6 = (0,           half)

    # draw hexagon points and fill in with colour
    points = [point1, point2, point3, point4, point5, point6]
    pygame.draw.polygon(surface, self.colour, points)

    # draw outline
    if self.drawEdges:
      pygame.draw.line(surface, BLACK, point1, point2, 1)
      pygame.draw.line(surface, BLACK, point2, point3, 1)
      pygame.draw.line(surface, BLACK, point3, point4, 1)
      pygame.draw.line(surface, BLACK, point4, point5, 1)
      pygame.draw.line(surface, BLACK, point5, point6, 1)
      pygame.draw.line(surface, BLACK, point6, point1, 1)

    return surface

'''
-----------------------------------------------
Hexagon shape for board
-----------------------------------------------
'''
class PathFinder:
  def __init__(self):
    self

'''
-----------------------------------------------
Main
-----------------------------------------------
'''
def HexGame_main():
  game = HexGame()
  game.main()
