import pygame

from hexBoy.hex.graphics.Colours import Colours

'''---
Hexagon shape for board
---'''
class HexagonGraphic:
    """Drawing of a hexagon"""

    def __init__(self, colour, size, drawEdges):
        """@param colour
        @param size
        
        """
        self.colour = colour
        self.hexSize = size
        self.drawEdges = drawEdges

    def getHexagon(self):
        """Get Hexagon drawing for pygame surface"""
        hexSize = self.hexSize
        surface = pygame.Surface((hexSize, hexSize))

        # fill in background and set it as the transparent colour
        surface.fill(Colours.WHITE)
        surface.set_colorkey(Colours.WHITE)

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
            pygame.draw.line(surface, Colours.BLACK, point1, point2, 1)
            pygame.draw.line(surface, Colours.BLACK, point2, point3, 1)
            pygame.draw.line(surface, Colours.BLACK, point3, point4, 1)
            pygame.draw.line(surface, Colours.BLACK, point4, point5, 1)
            pygame.draw.line(surface, Colours.BLACK, point5, point6, 1)
            pygame.draw.line(surface, Colours.BLACK, point6, point1, 1)

        return surface
