import pygame

"""
Improvements
- Populate the space with the current turn and who is playing (agent, player)
- Work on a graphic for the pathfinder to show paths and costs and other ways
  to visualize the algorithm
- Visualize pathfinder looking around
    Modify to show paths from the pathfinder board
"""

# COLOURS  R    G    B
WHITE =     (255, 255, 255)
BLACK =     (  0,   0,   0)
RED =       (255,   0,   0)
BLUE =      (  0,   0, 255)
DARK_RED =  (150,   0,   0)
DARK_BLUE = (  0,   0, 150)
# ty https://github.com/ThomasRush/py_a_star for the Hexagon rendering ideas
'''----------------------------------
Hex Graphics
----------------------------------'''
class HexGraphics:
    def __init__(self, boardSize=11, hexSize=40):
        self.hexSize = hexSize  # Hexagon size in pixels
        self.boardSize = boardSize  # Board size in Hexagons
        self.caption = "Hex Game"

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.xWindowLength = 400
        self.yWindowLength = 700 # TODO rename yWindowHeight
        self.screen = pygame.display.set_mode((self.xWindowLength, self.yWindowLength))

        # TODO move these inside an object: HexDrawings and each colour just "Blue"
        self.hexBlue = Hexagon(BLUE, self.hexSize, True)
        self.hexRed = Hexagon(RED, self.hexSize, True)
        self.hexWhite = Hexagon(WHITE, self.hexSize, True)
        self.hexBlueEdge = Hexagon(BLUE, self.hexSize, False)
        self.hexRedEdge = Hexagon(RED, self.hexSize, False)
        self.hexBlack = Hexagon(BLACK, self.hexSize, False)
        self.hexBlueWin = Hexagon(DARK_BLUE, self.hexSize, True)
        self.hexRedWin = Hexagon(DARK_RED, self.hexSize, True)

    def setupWindow(self): 
        pygame.display.set_caption(self.caption)
        self.screen.fill(WHITE)

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
                if (x == 0 and y == 0) or (
                    x == (boardSize + 1) and y == (boardSize + 1)
                ):
                    self.screen.blit(self.hexBlack.getHexagon(), (xPos, yPos))
                elif x == 0 or (x == (boardSize + 1)):
                    self.screen.blit(self.hexRedEdge.getHexagon(), (xPos, yPos))
                else:
                    self.screen.blit(self.hexBlueEdge.getHexagon(), (xPos, yPos))

        pygame.display.flip()

    # Put the hexagons on the board
    def updateWindow(self, gameBoard, winPath=[]):
        board = gameBoard.getNodeDict()

        boardSize = self.boardSize
        hexSize = self.hexSize
        borderOffset = hexSize / 2  # Extra space between screen border and hexagons

        # TODO This loop is basically the same as the one before. 
        # TODO maybe split this into render edges and inside
        # draw hexagons
        for x in range(boardSize):
            for y in range(boardSize):
                cell = (x, y)

                xPos = x * hexSize + borderOffset
                yPos = y * hexSize + borderOffset

                # offset yPos. Each column is half lower than previous
                yPos += x * (hexSize / 2)
                # offset xPos. Each row is quarter more to the left
                xPos -= x * (hexSize / 4)

                # Render the hex based on board position
                if board[cell].type == 1:
                    self.screen.blit(self.hexBlue.getHexagon(), (xPos, yPos))
                elif board[cell].type == 2:
                    self.screen.blit(self.hexRed.getHexagon(), (xPos, yPos))
                else:
                    self.screen.blit(self.hexWhite.getHexagon(), (xPos, yPos))

        # Draw path if supplied
        if winPath != None and len(winPath) != 0:
            for pos in winPath:

                cell = (pos[0], pos[1])

                xPos = pos[0] * hexSize + borderOffset
                yPos = pos[1] * hexSize + borderOffset

                # offset yPos. Each column is half lower than previous
                yPos += pos[0] * (hexSize / 2)
                # offset xPos. Each row is quarter more to the left
                xPos -= pos[0] * (hexSize / 4)

                if board[cell].type == 1:
                    self.screen.blit(self.hexBlueWin.getHexagon(), (xPos, yPos))
                elif board[cell].type == 2:
                    self.screen.blit(self.hexRedWin.getHexagon(), (xPos, yPos))
                elif not (board[cell].type == 3 or board[cell].type == 4):
                    self.screen.blit(self.hexBlueWin.getHexagon(), (xPos, yPos))

        pygame.display.flip()

        self.clock.tick(self.fps)

    def findHexagonCoordsForMousePos(self, mousePos):  
        """Return the Hex coords for a mouse click"""
        # Right now I'll basically create a rectangle grid to get a rough estimate
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

        (xMouse, yMouse) = mousePos
        hexSize = self.hexSize

        # TODO I feel like most of these offsets, widths and heights are used in a bunch of areas
        # Extra space between screen border and hexagons
        borderOffset = (hexSize / 2) + (hexSize / 8)
        rectWidth = hexSize * (3 / 4)  # using rectangles to estimate the hexagons
        rectHeight = hexSize

        # adjust for left border and divide by the rectangle width to get x value
        xMouseAdjusted = xMouse - borderOffset
        xRow = xMouseAdjusted // rectWidth

        # adjust for top border
        # account for offset y coords of columns as rows increase
        # divide by rectangle height to get y value
        yMouseAdjusted = yMouse - borderOffset
        yMouseAdjusted -= xRow * rectHeight / 2
        yRow = yMouseAdjusted // rectHeight

        # make sure type int
        return (int(xRow), int(yRow))

'''---
Hexagon shape for board
---'''
class Hexagon:
    # TODO description
    # TODO I like when the variables are define before init, also do types
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

        half = hexSize / 2  # half of the hexagon size
        qter = hexSize / 4  # quarter of the hexagon size

        # Hexagon points
        #  1 2
        # 6   3
        #  5 4
        point1 = (qter, 0)
        point2 = (3 * qter, 0)
        point3 = (hexSize - 1, half)
        point4 = (3 * qter, hexSize - 1)
        point5 = (qter, hexSize - 1)
        point6 = (0, half)

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
