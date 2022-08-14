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

def test_EmptyBoardNoWeakConnections(tmpdir):
    """Empty Board"""
    
    connections = GetConnections(tmpdir.board, 1)

    # Check weak connections
    expected = []
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = []
    actual = connections[1]
    assert set(actual) == set(expected)

def test_OneWeakConnection(tmpdir):
    """Two Hexes One connection"""
    
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)
    
    connections = GetConnections(tmpdir.board, 1)

    # Check weak connections
    expected = [(5,6)]
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = []
    actual = connections[1]
    assert set(actual) == set(expected)

def test_TwoWeakConnections(tmpdir):
    """Three Hexes Two connection"""
    
    tmpdir.board.makeMove((5,3), 1)
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)
    
    connections = GetConnections(tmpdir.board, 1)
    expected = [
        (5,6), 
        (5,4)
    ]
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = []
    actual = connections[1]
    assert set(actual) == set(expected)

def test_TwoHexesNoConnections(tmpdir):
    """Two Hexes no connection"""
    
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((2,2), 1)
    
    connections = GetConnections(tmpdir.board, 1)

    # Check weak connections
    expected = []
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = []
    actual = connections[1]
    assert set(actual) == set(expected)

def test_BlockingConnectionMove(tmpdir):
    """One opp move blocking connection"""
    
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,6), 2)
    tmpdir.board.makeMove((5,7), 1)
    
    connections = GetConnections(tmpdir.board, 1)

    # Check weak connections
    expected = []
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = []
    actual = connections[1]
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
    
    connections = GetConnections(tmpdir.board, 1)

    # Check weak connections
    expected = [
        (2,9),
        (4,8), 
        (5,4), (5,6)
    ]
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = []
    actual = connections[1]
    assert set(actual) == set(expected)

def test_BigClusterConnections(tmpdir):
    """Board with many moves from one player connected to each other """
    moves = [
        (4,5), (4,6),
        (5,4), (5,5), (5,6),
        (6,4), (6,5)
    ]
    for m in moves:
        tmpdir.board.makeMove(m, 1)

    connections = GetConnections(tmpdir.board, 1)

    # Check weak connections
    expected = []
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = []
    actual = connections[1]
    assert set(actual) == set(expected)

def test_OneStrongConnection(tmpdir):
    """One Strong move"""

    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((6,6), 1)
    
    connections = GetConnections(tmpdir.board, 1)

    # Check weak connections
    expected = []
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = [
        (5,6),
        (6,5)
    ]
    actual = connections[1]
    assert set(actual) == set(expected)

def test_TriangleConnection(tmpdir):
    """Three moves in a triangle connection"""

    tmpdir.board.makeMove((4,7), 1)
    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((6,6), 1)
    
    connections = GetConnections(tmpdir.board, 1)
    
    # Check strong connections
    expected = [
        (4,6),
        (5,6), (5,7),
        (6,5)
    ]
    actual = connections[1]
    assert set(actual) == set(expected)

def test_ComplexConnections(tmpdir):
    """A bunch of moves with strong and weak connections"""

    moves = [
        (2,4),
        (3,3), (3,6),
        (4,7),
        (5,1), (5,3), (5,5),
        (6,1),
        (7,4),
        (9,3)
    ]
    for m in moves:
        tmpdir.board.makeMove(m, 1)

    connections = GetConnections(tmpdir.board, 1)

    # Check weak connections
    expected = [
        (4,2), (4,3), 
        (5,4)
    ]
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = [
        (3,7),
        (4,5), (4,6),
        (5,2), (5,6),
        (6,2), (6,4), (6,5),
        (8,3), (8,4)
    ]
    actual = connections[1]
    assert set(actual) == set(expected)

def test_ComplexConnectionsWithOpponentMove(tmpdir):
    """A bunch of moves with strong and weak connections"""

    moves = [
        (2,4),
        (3,3), (3,6),
        (4,7),
        (5,1), (5,3), (5,5),
        (6,1),
        (7,4),
        (9,3)
    ]
    for m in moves:
        tmpdir.board.makeMove(m, 1)

    # OppMove
    tmpdir.board.makeMove((6,4), 2)
    
    connections = GetConnections(tmpdir.board, 1)

    # Check weak connections
    expected = [
        (4,2), (4,3), 
        (5,4),
        (6,5)
    ]
    actual = connections[0]
    assert set(actual) == set(expected)

    # Check strong connections
    expected = [
        (3,7),
        (4,5), (4,6),
        (5,2), (5,6),
        (6,2),
        (8,3), (8,4)
    ]
    actual = connections[1]
    assert set(actual) == set(expected)
    