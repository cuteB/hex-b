import pytest
from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.node.HexNode import HexNode
from hexBoy.hex.game.HexGameRules import HexGameRules

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    def sortFunc(item):
        return item[1].getPC()

    tmpdir.start = HexGameRules.blue.start
    tmpdir.end = HexGameRules.blue.end
    tmpdir.board = HexBoard()
    tmpdir.pf = PathBoy(
        tmpdir.board,
        HexGameRules.getCheckIfBarrierFunc(1),
        HexGameRules.getHeuristicFunc(1),
        sortFunc
    )

    # ^^^ before ^^^
    yield # run the rest
    # vvv After vvv

def test_EmptyBoardPath(tmpdir):
    """Test Empty Board Path Cost"""
    board = tmpdir.board
    bestPath = tmpdir.pf.findPath(
        tmpdir.start, 
        tmpdir.end
    )

    pathCost = tmpdir.pf.scorePath(bestPath)

    assert pathCost == 11
    assert bestPath == [
        (5,-1),
        (5,0),
        (5,1),
        (5,2),
        (5,3),
        (5,4),
        (5,5),
        (5,6),
        (5,7),
        (5,8),
        (5,9),
        (5,10),
        (5,11)
    ]

def test_OnePlayerNodePath(tmpdir):
    """Test Path cost with one node"""
    board = tmpdir.board
    board.makeMove(1, (1,1))

    bestPath = tmpdir.pf.findPath(
        tmpdir.start, 
        tmpdir.end
    )

    pathCost = tmpdir.pf.scorePath(bestPath)

    assert pathCost == 10
    assert bestPath == [
        (5, -1), 
        (4, -1), 
        (3, -1), 
        (2, 0), 
        (1, 1), 
        (1, 2), 
        (1, 3), 
        (1, 4), 
        (1, 5), 
        (1, 6), 
        (1, 7), 
        (1, 8), 
        (1, 9), 
        (1, 10), 
        (1, 11), 
        (2, 11), 
        (3, 11), 
        (4, 11), 
        (5, 11)
    ]


def test_PlayerPath(tmpdir):
    """Test Path Cost with winning Path"""
    board = tmpdir.board

    for i in range(11):
        board.makeMove(1, (0,i))

    bestPath = tmpdir.pf.findPath(
        tmpdir.start, 
        tmpdir.end
    )

    pathCost = tmpdir.pf.scorePath(bestPath)

    assert pathCost == 0
    assert bestPath == [
        (5,-1),
        (4,-1),
        (3,-1),
        (2,-1),
        (1,-1),
        (0,0),
        (0,1),
        (0,2),
        (0,3),
        (0,4),
        (0,5),
        (0,6),
        (0,7),
        (0,8),
        (0,9),
        (0,10),
        (0,11),
        (1,11),
        (2,11),
        (3,11),
        (4,11),
        (5,11)
    ]

def test_DifferentStartEndPath(tmpdir):
    """Path with different start and end points"""
    board = tmpdir.board

    for i in range(11): # TODO come back what is this test
        board.makeMove(1, (0,i))

    bestPath = tmpdir.pf.findPath(
        (4,6),
        (7,3),
    )


    assert bestPath == [(4,6),(5,5),(6,4),(7,3)]

def test_OpponentPath(tmpdir):
    """Test Cost When Opponent Wins"""
    board = tmpdir.board

    for i in range(11):
        board.makeMove(2, (i,0))

    bestPath = tmpdir.pf.findPath(
        tmpdir.start, 
        tmpdir.end
    )

    assert bestPath == []

def test_WinPathFound(tmpdir):
    """Check best Path with given moves"""
    board = tmpdir.board

    for i in range(11):
        board.makeMove(1, (5,i))

    bestPath = tmpdir.pf.findPath(
        tmpdir.start, 
        tmpdir.end
    )

    assert bestPath == [
        (5,-1),
        (5,0),
        (5,1),
        (5,2),
        (5,3),
        (5,4),
        (5,5),
        (5,6),
        (5,7),
        (5,8),
        (5,9),
        (5,10),
        (5,11)
    ]
