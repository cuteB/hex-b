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
    expected = [((5,6), 1)]

def test_TwoWeak(tmpdir):
    """Three Hexes Two connection"""
    expected = [((5,6), 1)]

