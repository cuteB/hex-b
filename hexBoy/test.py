from hexGame.HexGame import HexGame_main
from hexGame.AI.GetAgent import GetAgent
from hexGame.pathfinder.PathBoy import PathBoy
from hexGame.HexBoard import Board
from hexGame.HexNode import HexNode
from hexGame.HexGraphics import Graphics

def test():

  def sortFunc(item):
    return item[1].g

  board = Board(11)
  pf = PathBoy(board.getAdjacentSpaces, 0, sortFunc)
  graphics = Graphics(board.boardSize, 40)
  graphics.setupWindow()

  # wall = 6
  # for i in range(wall):
  #   board.makeMove((i,10), 2)


  num = pf.NumBestPaths(
    board.getNodeDict(),
    board.blueStartSpace, board.blueEndSpace,
    HexNode.checkIfBlueBarrierForAI,
    HexNode.getCellValueForNextMove
  )

  path = pf.findPath(
    board.getNodeDict(),
    board.blueStartSpace,
    board.blueEndSpace,
    HexNode.checkIfBlueBarrierForAI,
    HexNode.getCellValueForWinningPath
  )


  graphics.updateWindow(board, path)



  # while True:
  #   a = 1


#-------------------------------------------
#   start
#-------------------------------------------
if __name__ == "__main__":
  test()
