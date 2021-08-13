# I don't like the pygame startup message so I hide
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import sys
from pygame.locals import *
from math import cos, sin, pi

# COLOURS  R    G    B
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)

'''
Main hex game class
'''
class HexGame:
  def __init__(self):
    pygame.init()

    boardSize = 11
    self.playing = True # game loop check
    self.graphics = Graphics(boardSize)
    self.board = Board(boardSize)

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

      if (event.type == MOUSEBUTTONDOWN):
        print(self.mousePos)


  def update(self):
    self.graphics.updateWindow(self.board)

  # Exit the game
  def terminateGame(self):
    self.playing = False

  def main(self):
    self.setupGame()

    # main game loop
    while self.playing:
      self.eventLoop()
      self.update()

'''
Game Board
'''
class Board:
  def __init__(self, size):
    self.boardSize = size
    self.matrix = self.initGameBoard()

  def initGameBoard(self):
    boardMatrix = [[None] * self.boardSize for i in range(self.boardSize)]

    for x in range(self.boardSize):
      for y in range(self.boardSize):
        boardMatrix[x][y] = Hexagon(WHITE, x, y)

    return boardMatrix

'''
All Graphics for the game
'''
class Graphics:
  def __init__(self, size):
    self.boardSize = size
    self.caption = "Hex Game"

    self.fps = 60
    self.clock = pygame.time.Clock()

    self.xWindowLength = 400
    self.yWindowLength = 700
    self.screen = pygame.display.set_mode(
      (self.xWindowLength, self.yWindowLength)
    )

  def setupWindow(self):
    pygame.display.set_caption(self.caption)


  def updateWindow(self, board):
    # Draw red and blue side of screen
    self.screen.fill(RED)
    pygame.draw.rect(self.screen, BLUE, (40, 0, 700, 250))
    pygame.draw.rect(self.screen, BLUE, (0, 400, 360, 400))

    size = self.boardSize

    # draw hexagons
    for x in range(size):
      for y in range(size):
        hex = board.matrix[x][y]
        hex.draw(self.screen)

    pygame.display.update()

    self.clock.tick(self.fps)

'''
Hexagon shape for board
'''
class Hexagon:
  def __init__(self, colour, xPos, yPos, player = None):
    self.colour = colour
    self.player = player
    self.xPos = xPos
    self.yPos = yPos
    self.xGap = 30
    self.yGap = 35
    self.rowYOffset = 20


  def draw(self, surface):
    v = 6     # Hexagon
    r = 20
    x = self.xGap * self.xPos + 50
    y = self.yGap * self.yPos + 50 + (self.xPos * self.rowYOffset)

    pygame.draw.polygon(surface, self.colour, [
        (x + r * cos(2 * pi * i / v), y + r * sin(2 * pi * i / v))
        for i in range(v)
    ])
    pygame.draw.lines(
      surface,
      BLACK,
      True,
      [(cos(i / v * pi * 2) * r + x, sin(i / v * pi * 2) * r + y) for i in range(0, v)])

def HexGame_main():

  game = HexGame()
  game.main()
