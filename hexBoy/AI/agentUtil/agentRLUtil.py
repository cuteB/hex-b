import copy
from hexBoy.hex.node.HexNode import Hex
from hexBoy.hex.board.HexBoard import HexBoard

# TODO come back and deal with this file

# TODO this is wrong for hexes,
def getDistanceToCenter(self, move): # TODO 
    (x, y) = move
    center = int(self.boardSize // 2)

    return abs(x - center) + abs(y - center)

# TODO All of these look like garbage. Only used by AgentRL so move to utility/AgentRLUtil. Will need to detach from the board and put a HexBoard instead of self in the signature. 

# FIXME these two functions are ugly and bad
# return a copy of the current board
def getBoardFromMove(board: HexBoard, move: Hex, player):
    boardCopy = HexBoard()
    dictCopy = copy.deepcopy(board.getNodeDict())
    boardCopy.setBoardDict(dictCopy)

    boardCopy.makeMove(move, player)

    return boardCopy

# return a list of possible moves in this board
def getPossibleMoves(board):
    possibleMoves = []

    for x in range(board.boardSize):
        for y in range(board.boardSize):
            if board.validateMove((x, y)):
                possibleMoves.append((x, y))

    return possibleMoves

def getPlayerMoves(board, player):
    playerMoves = []
    for move in board.moveHistory:
        if board.boardDict[move[0]].type == player:  # FIXME Key Error
            playerMoves.append(move[0])

    return playerMoves

def syncBoard(board, parentBoard, moveCallback=None):
    """Sync the current board to the parent board based on move history"""
    parentMoveLen = len(parentBoard.moveHistory)
    selfMoveLen = len(board.moveHistory)

    for i in range(selfMoveLen, parentMoveLen):
        move = parentBoard.moveHistory[i]
        board.makeMove(move[0], move[1])

        if moveCallback != None:
            moveCallback(move)
