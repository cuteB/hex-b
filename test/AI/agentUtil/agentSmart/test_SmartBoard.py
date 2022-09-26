import pytest

from hexBoy.AI.agentUtil.agentSmart.SmartBoard import SmartBoard

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""

    tmpdir.board = SmartBoard(1)

    # ^^^ before ^^^
    yield # run the rest
    # vvv after vvv

def test_EmptySmartBoardTotalPaths(tmpdir):
    """Empty board paths for a player"""
    
    assert tmpdir.board.getNumPaths() == 6144

def test_SmartBoardWithMiddleMove(tmpdir):
    """Board with the move in the middle"""

    tmpdir.board.makeMove(1, (5,5))

    assert tmpdir.board.getNumPaths() == 1024
    assert tmpdir.board.getNumPathsToHex((5,5)) == 64
    assert tmpdir.board.getNumPathsFromHex((5,5)) == 64

def test_SmartBoardWithTwoMoves(tmpdir):
    """Board with the move in the middle"""

    tmpdir.board.makeMove(1, (5,5))
    tmpdir.board.makeMove(1, (4,7))
    
    assert tmpdir.board.getNumPaths() == 512
    assert tmpdir.board.getNumPathsToHex((5,5)) == 64
    assert tmpdir.board.getNumPathsFromHex((4,7)) == 8



