import pygame

# COLOURS  R    G    B
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)
DARK_RED = (150, 0, 0)
DARK_BLUE = (0,0,150)
'''
-----------------------------------------------
All Graphics drawing hexagons on a board
-----------------------------------------------
'''
# ty https://github.com/ThomasRush/py_a_star for the Hexagon rendering ideas
class Graphics:
  def __init__(self, boardSize, hexSize):
    self.hexSize = hexSize        # Hexagon size in pixels
    self.boardSize = boardSize         # Board size in Hexagons
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
