import pytest

from hexBoy.hex.HexBoard import Board
from hexBoy.AI.agentUtil.agentSmart.GetConnections import GetWeakConnections

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.size = 11
    tmpdir.board = Board(tmpdir.size)

    # ^^^ before ^^^
    yield # run the rest
    # vvv after vvv

def test_EmptyBoardNoConnections(tmpdir):
    """Empty Board"""
    expected = []
    actual = GetWeakConnections(tmpdir.board, 1)
    assert actual == expected

def test_OneWeakConnection(tmpdir):
    """Two Hexes One connection"""
    
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)
    
    expected = [(5,6)]
    actual = GetWeakConnections(tmpdir.board, 1)
    assert actual == expected


def test_TwoWeakConnections(tmpdir):
    """Three Hexes Two connection"""
    
    tmpdir.board.makeMove((5,3), 1)
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)
    
    expected = [
        (5,6), 
        (5,4)
    ]
    actual = GetWeakConnections(tmpdir.board, 1)
    assert actual == expected

def test_BlockingConnectionMove(tmpdir):
    """One opp move blocking connection"""
    
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)
    tmpdir.board.makeMove((5,6), 2)

    
    expected = []
    actual = GetWeakConnections(tmpdir.board, 1)
    assert actual == expected

def test_OneStrongConnection(tmpdir):
    """One Strong move"""

    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((6,7), 1)
    
    expected = [
        (5,6),
        (6,5)
    ]
    actual = GetWeakConnections(tmpdir.board, 1)
    assert actual == expected




