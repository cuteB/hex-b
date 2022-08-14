import copy
from typing import List
from dataclasses import dataclass
from hexBoy.hex.HexNode import HexNode

"""
Changes
- Need to modify the board to help out the pathfinder
- Each agent needs to modify values of the nodes to save time
- Need to get available moves and future states quick without breaking the
    board for the other player
- IDEA commit the current board to mem. then make moves to find future states
- then reset board to last commit or commit the next move

Needs to be faster for pathfinder
- Need to look deeper faster

IDEA: make a board for pathfinders to modify values for their nodes
"""

'''----------------------------------
Hex Board
----------------------------------'''
# TODO change name to hexboard
@dataclass
class Board:
    boardDict: dict  # dict<HexNode>, Cells on the board and their values
    boardSize: int  # int, size of the board
    moveHistory: List[tuple]  # ((x,y), player)[]

    # HexNode.Space, object of the different types of hex spaces.
    hexTypes: any

    # tuples of the (x,y) coordinates of the red/blue start/end spaces
    redStartSpace: tuple
    redEndSpace: tuple
    blueStartSpace: tuple
    blueEndSpace: tuple

    def __init__(self, boardSize=11):
        self.boardSize = boardSize
        self.hexTypes = HexNode.SpaceTypes
        self.moveHistory = []

        self.redStartSpace = (-1, 5)
        self.redEndSpace = (self.boardSize, 5)
        self.blueStartSpace = (5, -1)
        self.blueEndSpace = (5, self.boardSize)

        self.boardDict = self.initGameBoard()

    # Return the board node dict
    def getNodeDict(self):
        return self.boardDict

    def initGameBoard(self):
        """Initialize the starting game board"""
        dict = {}

        # initialize playing spaces
        for x in range(self.boardSize):
            for y in range(self.boardSize):
                dict[(x, y)] = HexNode(self.hexTypes.EMPTY, (x, y))

        # Itialize edges in dict
        # blue edge
        for x in range(self.boardSize):
            dict[(x, -1)] = HexNode(self.hexTypes.BLUE_EDGE, (x, -1))
            dict[(x, self.boardSize)] = HexNode(
                self.hexTypes.BLUE_EDGE, (x, self.boardSize)
            )
        # red edge
        for y in range(self.boardSize):
            dict[(-1, y)] = HexNode(self.hexTypes.RED_EDGE, (-1, y))
            dict[(self.boardSize, y)] = HexNode(
                self.hexTypes.RED_EDGE, (self.boardSize, y)
            )

        return dict

    def setBoardDict(self, dict):
        self.boardDict = dict

    def validateMove(self, cell) -> List[tuple]:
        """Check if the given cell is a valid move. (hex is empty)"""
        return (
            cell != None
            and self.isSpaceWithinBounds(cell)
            and self.boardDict[cell].type == self.hexTypes.EMPTY
        )

    # Make the move on the board dict, add to move history
    def makeMove(self, cell, player):
        """Make a move on the board and save it in history"""
        self.moveHistory.append((cell, player))
        self.boardDict[cell].setSpaceType(player)

    # Check if the move is within the board or edges
    def isSpaceWithinBounds(self, cell):
        boardSize = self.boardSize
        (x, y) = cell

        # include the edges around the matrix, cells within [-1, boardsize] bound.
        return (
            x >= -1
            and y >= -1
            and x <= boardSize
            and y <= boardSize
            # Don't include (-1,-1), (-1, len), (len, -1), (len, len)
            and not ((x == -1 or x == boardSize) and (y == -1 or y == boardSize))
        )

    def getAdjacentSpaces(self, cell):
        """Get the Hexes touching the gives Cell"""
        # Checkout /wiki/hex/board for the board with coordinates
        x = cell[0]
        y = cell[1]

        # eg for cell       (1,1)
        adjacentSpaces = []
        potentialSpaces = [
            (x, y - 1),  # (1,0) up
            (x, y + 1),  # (1,2) down
            (x - 1, y),  # (0,1) left
            (x + 1, y),  # (2,1) right
            (x - 1, y + 1),  # (0,2) down+left
            (x + 1, y - 1),  # (2,0) up+right
        ]

        # validate the potential spaces and return the adjacent spaces
        for space in potentialSpaces:
            if self.isSpaceWithinBounds(space):
                adjacentSpaces.append(space)

        return adjacentSpaces

    # XXX Don't really like this anymore. Remove it probably
    def get2AwaySpaces(self, cell):
        """Return spaces that are 2 away from the cell"""
        x = cell[0]
        y = cell[1]

        adjacentSpaces = []
        potentialSpaces = [
            (x - 2, y),
            (x - 2, y + 1),
            (x - 2, y + 2),
            (x - 1, y - 1),
            (x - 1, y + 2),
            (x, y - 2),
            (x, y + 2),
            (x + 1, y + 1),
            (x + 1, y - 2),
            (x + 2, y),
            (x + 2, y - 1),
            (x + 2, y - 2),
        ]

        # validate the potential spaces and return the adjacent spaces
        for space in potentialSpaces:
            if self.isSpaceWithinBounds(space):
                adjacentSpaces.append(space)

        return adjacentSpaces


    def resetGame(self):
        """Reset the board and move history"""
        self.boardDict = self.initGameBoard()
        self.moveHistory = []

    '''---
    Functions for moves
    ---'''
    # TODO this is wrong for hexes,
    def getDistanceToCenter(self, move):
        (x, y) = move
        center = int(self.boardSize // 2)

        return abs(x - center) + abs(y - center)

    def getPlayerMoves(self, playerId):
        """Look at the move history and return a player's moves"""
        playerMoves = []
        for i in range(len(self.moveHistory)):
            if self.moveHistory[i][1] == playerId:
                playerMoves.append(self.moveHistory[i][0])

        return playerMoves

    def getPlayerEndZone(self, player):
        """Get the end zone hexes of the player"""

        playerEndZone = []
        if (player == 1): 
            # blue edge
            for x in range(self.boardSize):
                playerEndZone.append((x, -1))
                playerEndZone.append((x, self.boardSize))

        else: 
            # red edge
            for y in range(self.boardSize):
                playerEndZone.append((-1, y))
                playerEndZone.append((self.boardSize, y))

        return playerEndZone


    '''---
    Functions for board
    ---'''
    # FIXME these two functions are ugly and bad
    # return a copy of the current board
    def getBoardFromMove(self, move, player):
        boardCopy = Board(self.boardSize)
        dictCopy = copy.deepcopy(self.getNodeDict())
        boardCopy.setBoardDict(dictCopy)

        boardCopy.makeMove(move, player)

        return boardCopy

    # return a list of possible moves in this board
    def getPossibleMoves(self):
        possibleMoves = []

        for x in range(self.boardSize):
            for y in range(self.boardSize):
                if self.validateMove((x, y)):
                    possibleMoves.append((x, y))

        return possibleMoves

    def getPlayerMoves(self, player):
        playerMoves = []
        for move in self.moveHistory:
            if self.boardDict[move[0]].type == player:  # FIXME Key Error
                playerMoves.append(move[0])

        return playerMoves

    def syncBoard(self, parentBoard, moveCallback=None):
        """Sync the current board to the parent board based on move history"""
        parentMoveLen = len(parentBoard.moveHistory)
        selfMoveLen = len(self.moveHistory)

        for i in range(selfMoveLen, parentMoveLen):
            move = parentBoard.moveHistory[i]
            self.makeMove(move[0], move[1])

            if moveCallback != None:
                moveCallback(move)
