import pytest
from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.HexBoard import Board
from hexBoy.hex.HexNode import HexNode

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
  """Reset the board and pathfinder before each test"""
  def sortFunc(item):
    return item[1].g

  tmpdir.board = Board(11)
  tmpdir.pf = PathBoy(
    tmpdir.board,
    tmpdir.board.getAdjacentSpaces,
    HexNode.checkIfBlueBarrierForAI,
    HexNode.getCellValueForNextMove,
    sortFunc
  )
  # ^^^ before ^^^
  yield # run the rest
  # vvv After vvv

def test_EmptyBoardPath(tmpdir):
  """Test Empty Board Path Cost"""
  board = tmpdir.board
  bestPath = tmpdir.pf.findPath(
    board.blueStartSpace,
    board.blueEndSpace,
  )

  pathCost = tmpdir.pf.ScorePath(bestPath)

  assert pathCost == 11

def test_OnePlayerNodePath(tmpdir):
  """Test Path cost with one node"""
  board = tmpdir.board
  board.makeMove((1,1), 1)

  bestPath = tmpdir.pf.findPath(
    board.blueStartSpace,
    board.blueEndSpace,
  )

  pathCost = tmpdir.pf.ScorePath(bestPath)

  assert pathCost == 10

def test_PlayerPath(tmpdir):
  """Test Path Cost with winning Path"""
  board = tmpdir.board

  for i in range(11):
    board.makeMove((0,i), 1)

  bestPath = tmpdir.pf.findPath(
    board.blueStartSpace,
    board.blueEndSpace,
  )

  pathCost = tmpdir.pf.ScorePath(bestPath)

  assert pathCost == 0

def test_OpponentPath(tmpdir):
  """Test Cost When Opponent Wins"""
  board = tmpdir.board

  for i in range(11):
    board.makeMove((i,0), 2)

  bestPath = tmpdir.pf.findPath(
    board.blueStartSpace,
    board.blueEndSpace,
  )

  pathCost = tmpdir.pf.ScorePath(bestPath)

  assert pathCost == 10000

def test_NumPathsEmptyBoard(tmpdir):
  """Test Number Of Paths on empty board"""
  board = tmpdir.board

  numPaths = tmpdir.pf.getNumBestPaths(
    board.blueStartSpace,
    board.blueEndSpace,
  )

  assert numPaths == 6144

def test_WinPathFound(tmpdir):
  """Check best Path with given moves"""
  board = tmpdir.board

  for i in range(11):
    board.makeMove((5,i), 1)

  bestPath = tmpdir.pf.findPath(
    board.blueStartSpace,
    board.blueEndSpace,
  )

  assert bestPath == [
    (5,10),
    (5,9),
    (5,8),
    (5,7),
    (5,6),
    (5,5),
    (5,4),
    (5,3),
    (5,2),
    (5,1),
    (5,0)
  ]
