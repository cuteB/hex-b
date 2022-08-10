import pytest

from hexBoy.hex.HexBoard import Board
from hexBoy.AI.agentUtil.agentSmart.GetConnections import GetConnections

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.size = 11
    tmpdir.board = Board(tmpdir.size)

    # ^^^ before ^^^
    yield # run the rest
    # vvv after vvv

def test_EmptyBoard(tmpdir):
    """Empty Board"""
    expected = []
    actual = GetConnections(tmpdir.board, 1)
    assert actual == expected

def test_OneWeak(tmpdir):
    """Two Hexes One connection"""
    
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)
    
    expected = [((5,6), 1)]
    actual = GetConnections(tmpdir.board, 1)
    assert actual == expected


def test_TwoWeak(tmpdir):
    """Three Hexes Two connection"""
    
    tmpdir.board.makeMove((5,3), 1)
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)
    
    expected = [
        ((5,6), 1), 
        ((5,4), 1)
    ]
    actual = GetConnections(tmpdir.board, 1)
    assert actual == expected

def test_BlockingMove(tmpdir):
    

def test_StrongMove(tmpdir):
    """One Strong move"""

    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((6,7), 1)
    
    expected = [
        ((5,6), 2),
        ((6,5), 2),
    ]
    actual = GetConnections(tmpdir.board, 1)
    assert actual == expected




