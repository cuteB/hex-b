import pytest

from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.node.HexNode import HexNode
from hexBoy.pathfinder.NumPathFinder import NumPathFinder

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""

    tmpdir.board = HexBoard()
    tmpdir.npf = NumPathFinder(tmpdir.board, 1)
    tmpdir.npf.initEmptyBoard()
    
    # ^^^ before ^^^
    yield # run the rest
    # vvv after vvv

def test_EmptySmartBoardNodePCDMiddle(tmpdir):
    """Nodes have PCD and family set"""

    # middle
    X: HexNode = tmpdir.board.getNodeDict()[(5,5)]
    assert X.getPath() == 5
    assert X.getDist() == 5
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(5,4), (6,4)])
    assert set(X.getSons()) == set([(4,6), (5,6)])

    # short edge 
    X = tmpdir.board.getNodeDict()[(10,3)]
    assert X.getPath() == 3
    assert X.getDist() == 7
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(10,2)])
    assert set(X.getSons()) == set([(9,4), (10,4)])

    # long edge
    X = tmpdir.board.getNodeDict()[(0,1)]
    assert X.getPath() == 1
    assert X.getDist() == 9
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(0,0), (1,0)])
    assert set(X.getSons()) == set([(0,2)])

    # start edge
    X = tmpdir.board.getNodeDict()[(2,0)]
    assert X.getPath() == 0
    assert X.getDist() == 10
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(2,-1)])
    assert set(X.getSons()) == set([(1,1), (2,1)])

    # end edge
    X = tmpdir.board.getNodeDict()[(4,10)]
    assert X.getPath() == 10
    assert X.getDist() == 0
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(4,9), (5,9)])
    assert set(X.getSons()) == set([(4,11)])

    # start end zone
    X = tmpdir.board.getNodeDict()[(5, -1)]
    assert set(X.getDads()) == set([])
    assert set(X.getSons()) == set([(5,0)])

    # end end zone
    X = tmpdir.board.getNodeDict()[(5, 11)]
    assert set(X.getDads()) == set([(5,10)])
    assert set(X.getSons()) == set([])

def test_MoreEmptySmartBoardNodePCDMiddle(tmpdir):
    """Testing more nodes, Some nodes might be acting funny"""

    X: HexNode = tmpdir.board.getNodeDict()[(6,6)]
    assert X.getPath() == 6
    assert X.getDist() == 4
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(6,5), (7,5)])
    assert set(X.getSons()) == set([(5,7), (6,7)])

    X: HexNode = tmpdir.board.getNodeDict()[(3,6)]
    assert X.getPath() == 6
    assert X.getDist() == 4
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(3,5), (4,5)])
    assert set(X.getSons()) == set([(2,7), (3,7)])

def test_EmptySmartBoardTotalPaths(tmpdir):
    """Empty board paths for a player"""

    assert tmpdir.npf.getNumPaths() == 6144
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((5,5)) == 32

def test_SmartBoardWithMiddleMove(tmpdir):
    """Board with the move in the middle"""

    tmpdir.board.makeMove(1, (5,5))
    tmpdir.npf.updateMove(1, (5,5))

    assert tmpdir.npf.getNumPaths() == 1024
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((5,5)) == 32

def test_SmartBoardWithTwoMoves(tmpdir):
    """Board with two strong moves"""

    moves = [(5,5), (4,7)]
    for m in moves:
        tmpdir.board.makeMove(1, m)
        tmpdir.npf.updateMove(1, m)

    
    assert tmpdir.npf.getNumPaths() == 512
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((4,7)) == 8

def test_SmartBoardWithThreeMoves(tmpdir):
    """Board with three strong moves"""

    moves = [(5,5), (4,7), (3,9)]
    for m in moves:
        tmpdir.board.makeMove(1, m)
        tmpdir.npf.updateMove(1, m)
    
    assert tmpdir.npf.getNumPaths() == 256
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((3,9)) == 2

def test_SmartBoardWithThreeMovesUpdateDad(tmpdir):
    """Board with three strong moves in a different place"""

    moves = [(5,5), (4,7), (6,3)]
    for m in moves:
        tmpdir.board.makeMove(1, m)
        tmpdir.npf.updateMove(1, m)
    
    assert tmpdir.npf.getNumPaths() == 256
    assert tmpdir.npf.getNumPathsToHex((6,3)) == 8
    assert tmpdir.npf.getNumPathsFromHex((4,7)) == 8