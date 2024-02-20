import pygame

from hexBoy.hex.graphics.Colours import Colours

'''---
Hexagon shape for board
---'''
class HexagonGraphic:
    """Drawing of a hexagon"""

    def __init__(self, colour, size, drawEdges, text = ""):
        self.colour = colour
        self.hexSize = size
        self.drawEdges = drawEdges
        self.text = text

    def getHexagon(self):
        """Get Hexagon drawing for pygame surface"""
        hexSize = self.hexSize
        surface = pygame.Surface((hexSize, hexSize))

        # COMEBACK This might be the reason that the render is super slow. Maybe the surface is rendering lots of layers
        # fill in background and set it as the transparent colour
        # For some reason OFF white fixes the text overwrite issue
        surface.fill(Colours.OFFWHITE)
        surface.set_colorkey(Colours.OFFWHITE)

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

        # Change colour if white and tracking the depth of each node
        # COMEBACK make this something


        # draw hexagon points and fill in with colour
        points = [point1, point2, point3, point4, point5, point6]
        pygame.draw.polygon(surface, self.colour, points)

        # draw outline on play area
        if self.drawEdges:
            pygame.draw.line(surface, Colours.BLACK, point1, point2, 1)
            pygame.draw.line(surface, Colours.BLACK, point2, point3, 1)
            pygame.draw.line(surface, Colours.BLACK, point3, point4, 1)
            pygame.draw.line(surface, Colours.BLACK, point4, point5, 1)
            pygame.draw.line(surface, Colours.BLACK, point5, point6, 1)
            pygame.draw.line(surface, Colours.BLACK, point6, point1, 1)
            
            # Put in text
            # TODO disable during non playground game
            font = pygame.font.Font('freesansbold.ttf', 15) # TODO change the text size based on the length of the text
            text = font.render(self.text, True, (0,0,0), self.colour)
            textRect = text.get_rect()
            textRect.center = (self.hexSize/2,self.hexSize/2)
            surface.blit(text, textRect)

        return surface
