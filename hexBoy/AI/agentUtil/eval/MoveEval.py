from hexBoy.AI.agentUtil.board.GetDistanceToCenter import GetDistanceToCenter
from hexBoy.hex.board.HexBoard import HexBoard

# COMEBACK This is old and needs to be updated

def evaluateMove(move, gameBoard, winPath, opponentPath, player):
    value = 1
    if isStrongMove(move, gameBoard, player):
        value += 2

    if move in winPath:
        value += 5

    if move in opponentPath:
        value += 3

    value += 8 - GetDistanceToCenter(move)

    return value

def isStrongMove(move, gameBoard: HexBoard, player):
    # This isn't the best
    playerMoves = gameBoard.getPlayerMoves(player)
    (x, y) = move
    strongMoves = [
        (x - 2, y + 1),
        (x - 1, y - 1),
        (x - 1, y + 2),
        (x + 1, y + 1),
        (x + 1, y - 2),
        (x + 2, y - 1),
    ]
    strongDict = {}
    strongDict[strongMoves[0]] = [(x - 1, y), (x - 1, y + 1)]
    strongDict[strongMoves[1]] = [(x - 1, y), (x, y - 1)]
    strongDict[strongMoves[4]] = [(x - 1, y + 1), (x, y + 1)]
    strongDict[strongMoves[3]] = [(x, y + 1), (x + 1, y)]
    strongDict[strongMoves[2]] = [(x + 1, y - 1), (x, y - 1)]
    strongDict[strongMoves[5]] = [(x + 1, y), (x + 1, y - 1)]

    potentialStrongMoves = []
    for sMove in strongMoves:
        if gameBoard.isSpaceWithinBounds(sMove):
            potentialStrongMoves.append(sMove)

    for strongMove in potentialStrongMoves:
        if strongMove in playerMoves:

            movesToStrongMove = strongDict[strongMove]
            if (
                not movesToStrongMove[0] in gameBoard.getMoveHistory()
                and not movesToStrongMove[1] in gameBoard.getMoveHistory()
            ):
                return True

    return False

# def spacesNearWinPath( winPath, gameBoard):
#   nearPath = {}
#
#   for space in winPath:
#     adjacentSpaces = self.getAdjacentSpaces(space)
#     for closeBy in adjacentSpaces:
#       nearPath[closeBy] = closeBy
#
#   return nearPath

# From agent strong?
def evaluateBoardMove(self, gameBoard):

    move = self.randomMove(gameBoard)
    moveVal = self.boardEval.evaluateBoard(gameBoard.moveHistory)

    for x in range(gameBoard.boardSize):
        for y in range(gameBoard.boardSize):
            nextMove = (x, y)
            if gameBoard.validateMove(nextMove):
                nextMoveHistory = gameBoard.moveHistory
                nextMoveHistory.append(nextMove)

                nextVal = self.boardEval.evaluateBoard(nextMoveHistory)
                if nextVal > moveVal:
                    moveVal = nextVal
                    move = nextMove

    return move
