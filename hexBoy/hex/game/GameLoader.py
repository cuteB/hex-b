from hexBoy.hex.graphics.HexGraphics import HexGraphics
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.db.HexDBConfig import HexLogger

# HACK Idk if this works
def loadBoardFromGameId(gameId: int) -> HexBoard:
    xLogger = HexLogger()

    moveList = xLogger.getMovesForGameId(gameId)
    board = HexBoard()

    for player, X in moveList:
        board.makeMove(player, X)

    return board

def testFunc():
    board = loadBoardFromGameId(3)

    graphics = HexGraphics()
    graphics.setupWindow(board)

    while True:
        graphics.updateWindow(board)
