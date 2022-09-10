import pytest

from hexBoy.hex.node.HexNode import Hex
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.AI.agentUtil.board.GetDistanceToCenter import GetDistanceToCenter

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.center = (5,5)
    tmpdir.board = HexBoard()

    # ^^^ before ^^^
    yield  # run the rest
    # vvv After vvv

def test_CenterDistanceIsZero(tmpdir):
    """Check that the distance to the center of the center hex is zero"""

    assert GetDistanceToCenter(tmpdir.center) == 0

def test_CenterDistanceOneAway(tmpdir):
    """Check the adjacent Hexes of the center are one away"""

    adjX = tmpdir.board.getAdjacentSpaces(tmpdir.center)

    for X in adjX:
        assert GetDistanceToCenter(X) == 1

def test_CenterDistanceFromCloseCorners(tmpdir):
    """Close corners are 5 away"""

    assert GetDistanceToCenter((0, 10)) == 5
    assert GetDistanceToCenter((10, 0)) == 5

def test_CenterDistanceFromFarCorners(tmpdir):
    """Far are 10 away"""

    assert GetDistanceToCenter((10, 10)) == 10
    assert GetDistanceToCenter((0, 0)) == 10

def test_CenterDistanceForAFewPickedHexes(tmpdir):
    """Distance for a few selected hexes"""
    assert GetDistanceToCenter((4, 8)) == 3
    assert GetDistanceToCenter((1, 7)) == 4
    assert GetDistanceToCenter((7, 9)) == 6
    assert GetDistanceToCenter((7, 9)) == 6
    assert GetDistanceToCenter((9, 3)) == 4

def test_CenterDistFromAnEdge(tmpdir):
    """Edges should still be able to have a distance to the center"""
    assert GetDistanceToCenter((5, -1)) == 6
    assert GetDistanceToCenter((1, -1)) == 10
    assert GetDistanceToCenter((9, -1)) == 6
    assert GetDistanceToCenter((-1, 6)) == 6