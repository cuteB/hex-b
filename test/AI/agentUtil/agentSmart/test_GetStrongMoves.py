import pytest

from hexBoy.hex.HexBoard import Board
from hexBoy.AI.agentUtil.agentSmart.GetStrongMoves import GetStrongMoves

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
    actual = GetStrongMoves(tmpdir.board, 1)
    assert actual == expected

def test_OneMoveBoard(tmpdir):
    """One player move"""
    tmpdir.board.makeMove((2,2), 1)

    expected = [(0,3), (1,1), (1,4), (3,0), (3,3), (4,1)]
    actual = GetStrongMoves(tmpdir.board, 1)
    assert set(actual) == set(expected)

def test_OneMoveEach(tmpdir):
    """board with a move from each player"""
    tmpdir.board.makeMove((2,2), 1)
    tmpdir.board.makeMove((5,5), 2)

    expected = [(0,3), (1,1), (1,4), (3,0), (3,3), (4,1)]
    actual = GetStrongMoves(tmpdir.board, 1)
    assert set(actual) == set(expected)

def test_OneMoveEachBeside(tmpdir):
    """Board with opp move beside player move"""
    tmpdir.board.makeMove((2,2), 1)
    tmpdir.board.makeMove((2,3), 2)

    expected = [(0,3), (1,1), (3,0), (4,1)]
    actual = GetStrongMoves(tmpdir.board, 1)
    assert set(actual) == set(expected)

def test_TwoMoves(tmpdir):
    """Board with two moves from the player"""
    tmpdir.board.makeMove((2,2), 1)
    tmpdir.board.makeMove((5,5), 1)

    expected = [(0,3), (1,1), (1,4), (3,0), (3,3), (3,6), (4,1), (4,4), (4,7), (6,3), (6,6), (7,4)]
    actual = GetStrongMoves(tmpdir.board, 1)
    assert set(actual) == set(expected)

def test_TwoMovesBeside(tmpdir):
    """Board with two moves from the player beside each other"""
    tmpdir.board.makeMove((2,2), 1)
    tmpdir.board.makeMove((2,3), 1)

    expected = [(0,3), (0,4), (1,1), (1,5), (3,0), (3,4), (4,1), (4,2)]
    actual = GetStrongMoves(tmpdir.board, 1)
    assert set(actual) == set(expected)

def test_TwoMovesClose(tmpdir):
    """Board with two moves from the player that are one space away in the same x coord"""
    tmpdir.board.makeMove((2,2), 1)
    tmpdir.board.makeMove((2,4), 1)

    expected = [(0,3), (0,5), (1,1), (1,6), (3,0), (3,5), (4,1), (4,3)]
    actual = GetStrongMoves(tmpdir.board, 1)
    assert set(actual) == set(expected)

def test_OneBigConnection(tmpdir):
    """Board with many moves from one player connected to each other """
    moves = [
        (4,4),
        (5,4), (5,5), (5,9),
        (6,5), (6,6), (6,7), (6,8)
    ]
    for m in moves:
        tmpdir.board.makeMove(m, 1)

    expected = [
        (2,5),
        (3,3), (3,6), (3,10),
        (4,7), (4,8), 
        (5,2),
        (6,2), (6,10),
        (7,3), (7,9),
        (8,4), (8,5), (8,6), (8,7)
    ]
    actual = GetStrongMoves(tmpdir.board, 1)
    assert set(actual) == set(expected)

def test_FiveNineEdgeCase(tmpdir):
    """(5,9) because I feel like the prev test is wrong, (i'm dumb)"""
    tmpdir.board.makeMove((5,9), 1)

    expected = [(3,10), (4,8), (6,7), (6,10), (7,8)]
    actual = GetStrongMoves(tmpdir.board, 1)
    assert set(actual) == set(expected)

def test_BigClusterStrongMoves(tmpdir):
    """Board with many moves from one player connected to each other """
    moves = [
        (4,5), (4,6),
        (5,4), (5,5), (5,6),
        (6,4), (6,5)
    ]
    for m in moves:
        tmpdir.board.makeMove(m, 1)

    expected = [
        (2,6), (2,7),
        (3,4), (3,8),
        (4,3), (4,8),
        (6,2), (6,7), 
        (7,2), (7,6),
        (8,3), (8,4)
    ]
    actual = GetStrongMoves(tmpdir.board, 1)
    assert set(actual) == set(expected)
