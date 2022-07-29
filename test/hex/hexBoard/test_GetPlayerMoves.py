import pytest

from hexBoy.hex.HexBoard import Board

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.size = 11
    tmpdir.board = Board(tmpdir.size)

    # ^^^ before ^^^
    yield # run the rest
    # vvv After vvv

def test_EmptyBoard(tmpdir):
    """Test Empty Board"""
    moves = tmpdir.board.getPlayerMoves(1)
    assert moves == []

def test_OneMove(tmpdir):
    """Test board with one player move"""
    expectedMoves = [(0,0)]

    for m in expectedMoves:
        tmpdir.board.makeMove(m, 1)

    actualMoves = tmpdir.board.getPlayerMoves(1)
    assert actualMoves == expectedMoves

def test_OpponentMove(tmpdir):
    """Test board with one opponent move"""
    expectedMoves = []
    oppMoves = [(0,0)]

    for m in expectedMoves:
        tmpdir.board.makeMove(m, 1)

    for m in oppMoves:
        tmpdir.board.makeMove(m, 2)

    actualMoves = tmpdir.board.getPlayerMoves(1)
    assert actualMoves == expectedMoves

def test_OneOfEachPlayerMove(tmpdir):
    """Test board with a move from each player"""
    expectedMoves = [(1,0)]
    oppMoves = [(0,0)]

    for m in expectedMoves:
        tmpdir.board.makeMove(m, 1)

    for m in oppMoves:
        tmpdir.board.makeMove(m, 2)

    actualMoves = tmpdir.board.getPlayerMoves(1)
    assert actualMoves == expectedMoves

def test_WholeBunchOfMoves(tmpdir):
    """Test board with A bunch of moves from each player"""
    expectedMoves = [(5,5), (8,2), (2,2)]
    oppMoves = [(0,0), (1,2), (9,9)]

    for m in expectedMoves:
        tmpdir.board.makeMove(m, 1)

    for m in oppMoves:
        tmpdir.board.makeMove(m, 2)

    actualMoves = tmpdir.board.getPlayerMoves(1)
    assert actualMoves == expectedMoves

    actualMoves = tmpdir.board.getPlayerMoves(2)
    assert actualMoves == oppMoves
