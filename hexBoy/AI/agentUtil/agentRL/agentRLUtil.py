import copy
from hexBoy.hex.node.HexNode import Hex
from hexBoy.hex.board.HexBoard import HexBoard

# TODO come back and deal with this file


# TODO All of these look like garbage. Only used by AgentRL so move to utility/AgentRLUtil. Will need to detach from the board and put a HexBoard instead of self in the signature. 

# FIXME these two functions are ugly and bad
# return a copy of the current board
def GetBoardFromMove(board: HexBoard, move: Hex, player: int):
    boardCopy = HexBoard()
    dictCopy = copy.deepcopy(board.getNodeDict())
    boardCopy.setNodeDict(dictCopy)

    boardCopy.makeMove(player, move)

    return boardCopy

# return a list of possible moves in this board
def GetPossibleMoves(board: HexBoard):
    possibleMoves = []

    for x in range(board.boardSize):
        for y in range(board.boardSize):
            if board.validateMove((x, y)):
                possibleMoves.append((x, y))

    return possibleMoves

def getPlayerMoves(board: HexBoard, player: int):
    playerMoves = []
    for move in board.getMoveHistory():
        if board.getNodeDict()[move[0]].getHexType().player == player:  # FIXME Key Error
            playerMoves.append(move[0])

    return playerMoves
