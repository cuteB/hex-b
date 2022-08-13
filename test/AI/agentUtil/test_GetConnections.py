import pytest

from hexBoy.hex.HexBoard import Board
from hexBoy.AI.agentUtil.agentSmart.GetConnections import GetConnections
from hexBoy.AI.agentUtil.agentSmart.GetConnections import GetConnections

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.size = 11
    tmpdir.board = Board(tmpdir.size)

    # ^^^ before ^^^
    yield # run the rest
    # vvv after vvv

'''---
Weak Connections
---'''

def test_EmptyBoardNoWeakConnections(tmpdir):
    """Empty Board"""
    expected = []
    connections = GetConnections(tmpdir.board, 1)
    actual = connections[0]
    assert set(actual) == set(expected)

def test_OneWeakConnection(tmpdir):
    """Two Hexes One connection"""
    
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)
    
    expected = [(5,6)]
    connections = GetConnections(tmpdir.board, 1)
    actual = connections[0]
    assert set(actual) == set(expected)

def test_TwoWeakConnections(tmpdir):
    """Three Hexes Two connection"""
    
    tmpdir.board.makeMove((5,3), 1)
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)
    
    expected = [
        (5,6), 
        (5,4)
    ]
    connections = GetConnections(tmpdir.board, 1)
    actual = connections[0]
    assert set(actual) == set(expected)

def test_TwoHexesNoConnections(tmpdir):
    """Two Hexes no connection"""
    
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((2,2), 1)
    
    expected = []
    connections = GetConnections(tmpdir.board, 1)
    actual = connections[0]
    assert set(actual) == set(expected)

def test_BlockingConnectionMove(tmpdir):
    """One opp move blocking connection"""
    
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,6), 2)
    tmpdir.board.makeMove((5,7), 1)
    
    expected = []
    connections = GetConnections(tmpdir.board, 1)
    actual = connections[0]
    assert set(actual) == set(expected)

def test_LongLineOfWeakConnections(tmpdir):
    """A bunch of hexes in a weak connection"""

    moves = [
        (1,9),
        (3,9),
        (5,3), (5,5), (5,7)
    ]
    for m in moves:
        tmpdir.board.makeMove(m, 1)
    
    expected = [
        (2,9),
        (4,8), 
        (5,4), (5,6)
    ]
    connections = GetConnections(tmpdir.board, 1)
    actual = connections[0]
    assert set(actual) == set(expected)

'''---
Strong Connections
---'''

def test_OneStrongConnection(tmpdir):
    """One Strong move"""

    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((6,6), 1)
    
    expected = [
        (5,6),
        (6,5)
    ]
    connections = GetConnections(tmpdir.board, 1)
    actual = connections[1]
    assert set(actual) == set(expected)

def test_TriangleConnection(tmpdir):
    """Three moves in a triangle connection"""

    tmpdir.board.makeMove((4,7), 1)
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((6,6), 1)
    
    expected = [
        (4,6),
        (5,6), (5,7),
        (6,5)
    ]
    connections = GetConnections(tmpdir.board, 1)
    actual = connections[1]
    assert set(actual) == set(expected)

'''---
Strong and Weak Connections
---'''

