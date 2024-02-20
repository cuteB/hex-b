import pygame
from typing import List, Callable
from dataclasses import dataclass

from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.graphics.Colours import Colours
from hexBoy.hex.graphics.HexagonGraphic import HexagonGraphic
from hexBoy.hex.node.HexNode import Hex, HexType, HexNode
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.models.SortedDict import SortedDict
"""
Improvements
- Populate the space with the current turn and who is playing (agent, player)
- Work on a graphic for the pathfinder to show paths and costs and other ways
  to visualize the algorithm
- Visualize pathfinder looking around
    Modify to show paths from the pathfinder board
"""

class Hexagons:
    """Hexagons used for rendering the Hex Game"""
    def __init__(self, hexSize):
        self.blue =  HexagonGraphic(Colours.BLUE, hexSize, True)
        self.red =  HexagonGraphic(Colours.RED, hexSize, True)
        self.white = HexagonGraphic(Colours.WHITE, hexSize, True)
        self.blueEdge = HexagonGraphic(Colours.BLUE, hexSize, False)
        self.redEdge = HexagonGraphic(Colours.RED, hexSize, False)
        self.black = HexagonGraphic(Colours.BLACK, hexSize, False)
        self.blueWin = HexagonGraphic(Colours.DARK_BLUE, hexSize, True)
        self.redWin = HexagonGraphic(Colours.DARK_RED, hexSize, True)

@dataclass
class GameDisplayOptions:
    name: int
    board: HexBoard
    getHexagonGraphic: Callable[[HexNode], HexagonGraphic]

DEFAULT_HEX_SIZE: int = 40
    

'''----------------------------------
Hex Graphics
----------------------------------'''
class HexGraphics:
    _hexSize: int
    _boardSize: int
    _caption: str
    
    _fps: int
    _clock: any
    _xWindowLength: int
    _yWindowHeight: int
    _screen: any
    _Hexagons: Hexagons

    """Graphics window for the Hex Game"""
    def __init__(self, boardSize=11, hexSize=DEFAULT_HEX_SIZE):
        self._hexSize = hexSize  # Hexagon size in pixels
        self._boardSize = boardSize  # Board size in Hexagons
        self._caption = "Hex Game"

        self._fps = 60
        self._clock = pygame.time.Clock()

        self._xWindowLength = 700
        self._yWindowHeight = 700 
        self._screen = pygame.display.set_mode((self._xWindowLength, self._yWindowHeight))

        self._Hexagons: Hexagons = Hexagons(hexSize=self._hexSize)


    '''---
    Private
    ---'''
    def _getHexPos(self, X: Hex) -> tuple:
        """Get the window pos given a Hex"""
        (x, y) = X
        hexSize: int = self._hexSize
        borderOffset: float = hexSize / 2  # Extra space between screen border and hexagons
        xPos = x * hexSize + borderOffset
        yPos = y * hexSize + borderOffset

        # offset yPos. Each column is half lower than previous
        yPos += x * (hexSize / 2)
        # offset xPos. Each row is quarter more to the left
        xPos -= x * (hexSize / 4)

        return (xPos, yPos)

    def _getHexagonGraphic(self, xType: HexType, inWinPath: bool, text: str = "") -> HexagonGraphic:
        """Return the Hexagons Graphic given a Hex Node"""

        if (xType.player == 1): # blue
            if (xType.xType == 1): # hex
                if (not inWinPath): # regular hex
                    # return self._Hexagons.blue
                    return HexagonGraphic(Colours.BLUE, self._hexSize, True, text)
                else: # win Hex
                    return self._Hexagons.blueWin
            else: # edge
                return self._Hexagons.blueEdge

        elif (xType.player == 2): # red
            if (xType.xType == 1): # hex
                if (not inWinPath): # regular hex
                    return HexagonGraphic(Colours.RED, self._hexSize, True, text)
                    # return self._Hexagons.red
                else: # win Hex
                    return self._Hexagons.redWin
            else: # edge
                return self._Hexagons.redEdge

        else: # White
            return  HexagonGraphic(Colours.WHITE, self._hexSize, True, text)
            # return self._Hexagons.white

    '''---
    Public
    ---'''
    def setupWindow(self, gameBoard: HexBoard) -> None:
        """Initialize the game board with edges and white hexes"""

        pygame.display.set_caption(self._caption)
        self._screen.fill(Colours.WHITE)
        self.updateWindow(gameBoard, [], True)

    def updateWindow(self, gameBoard: HexBoard, winPath: List[Hex]=[], renderEdges: bool = False, extraBoards: List[SortedDict] = None, displayBoards: List[GameDisplayOptions] = []):
        """Update the Game Window"""
        # nodeDict: dict = gameBoard.getNodeDict()

        # new start
        if len(displayBoards) > 0:
            currentDisplayBoard:GameDisplayOptions = displayBoards[0]
            nodeDict: dict = currentDisplayBoard.board.getNodeDict()
            _getHexagonGraphic = currentDisplayBoard.getHexagonGraphic 
        else:

            nodeDict: dict = gameBoard.getNodeDict()
            _getHexagonGraphic = getDefaultHexagonGraphic

        # Render Board Nodes
        for key in nodeDict:
            X: HexNode = nodeDict[key]

            # TODO the rest of this function can probably go into a modular function that only needs the HexNode to provide what should be displayed. The render edge check should probably stay but other than that all of this should be changeable. 

            xType = X.getHexType()
            # if (xType.xType == 1 or renderEdges): # always render hexes, sometimes render edges

                # def temp_getHexagonGraphic(X: HexNode):
                #     inWinPath = (winPath != None and X in winPath)

                #     value = ""
                #     if nodeDict != None:
                #         if nodeDict[key].getHexType().player != 1 and extraBoards != None: #TODO change this to only show playable hexes for a certain player. Need to have the graphics "Display for a certain player". This line will prevent blue hexes from having text
                #             agentDict: SortedDict = extraBoards[0]

                #             value = str(agentDict[key].getPathsToNode()) 

                #     return self._getHexagonGraphic(xType, inWinPath, value).getHexagon()

            pos = self._getHexPos(X)
            # self._screen.blit(_getHexagonGraphic(X).getHexagon(), pos)
            self._screen.blit(_getHexagonGraphic(X).getHexagon(), pos)
                

        # Render Black spaces
        if (renderEdges): 
            for X in [(-1, -1), (-1, 11), (11, -1), (11, 11)]:
                pos = self._getHexPos(X)
                self._screen.blit(self._Hexagons.black.getHexagon(), pos)

        pygame.display.flip()

    def findHexagonCoordsForMousePos(self, mousePos) -> Hex:  
        """Return the Hex coords for a mouse click"""
        # Right now I'll basically create a rectangle grid to get a rough estimate
        # of what cell was clicked. Will work fine when the user clicks in the middle
        #
        # Using Rectangles to estimate the hexagon
        # - Height = Hexagon Size
        # - Width = Hexagon Size * 3/4 (Need to account for interlock)
        #
        # Note: values used in this function are slightly different than the rendering
        # function due to using rectangles and not Hexes
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
        hexSize = self._hexSize

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
    
def getDefaultHexagonGraphic(X: HexNode) -> HexagonGraphic:
    _hexSize = DEFAULT_HEX_SIZE
    _Hexagons: Hexagons = Hexagons(_hexSize)

    player = X.getHexType().player
    xType = X.getHexType().xType
    inWinPath = X.getBest() == 0

    if (player == 1): # blue
        if (xType == 1): # hex
            if (not inWinPath): # regular hex
                # return self._Hexagons.blue
                return HexagonGraphic(Colours.BLUE,_hexSize, True)
            else: # win Hex
                return _Hexagons.blueWin
        else: # edge
            return _Hexagons.blueEdge

    elif (player == 2): # red
        if (xType == 1): # hex
            if (not inWinPath): # regular hex
                return HexagonGraphic(Colours.RED,_hexSize, True)
                # return self._Hexagons.red
            else: # win Hex
                return _Hexagons.redWin
        else: # edge
            return _Hexagons.redEdge

    else: # White
        return  HexagonGraphic(Colours.WHITE, _hexSize, True)
        # return self._Hexagons.white


# ty https://github.com/ThomasRush/py_a_star for the Hexagon rendering ideas
