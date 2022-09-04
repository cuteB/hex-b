import pytest

from hexBoy.hex.game.HexGameRules import HexGameRules
from hexBoy.hex.board.HexBoard import HexBoard

# TODO move to test/hex/game
@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.board = HexBoard()

    # ^^^ before ^^^
    yield # run the rest
    # vvv After vvv

def test_EmptyBoardHexTypes(tmpdir):
    """Default Board types"""
    X = (5,5)
    bEdge = (5,-1)
    rEdge = (-1,5)

    assert tmpdir.board.getNodeDict()[X].getHexType() == HexGameRules.empty.hex
    assert tmpdir.board.getNodeDict()[bEdge].getHexType() == HexGameRules.blue.edge
    assert tmpdir.board.getNodeDict()[rEdge].getHexType() == HexGameRules.red.edge

def test_HexTypesAfterMakingMoves(tmpdir):
    """Making moves changes the Hex Types on the board"""
    bX = (4,5)
    rX = (5,5)

    assert tmpdir.board.getNodeDict()[bX].getHexType() == HexGameRules.empty.hex
    assert tmpdir.board.getNodeDict()[rX].getHexType() == HexGameRules.empty.hex

    tmpdir.board.makeMove(1,bX)
    assert tmpdir.board.getNodeDict()[bX].getHexType() == HexGameRules.blue.hex
    assert tmpdir.board.getNodeDict()[rX].getHexType() == HexGameRules.empty.hex

    tmpdir.board.makeMove(2,rX)
    assert tmpdir.board.getNodeDict()[bX].getHexType() == HexGameRules.blue.hex
    assert tmpdir.board.getNodeDict()[rX].getHexType() == HexGameRules.red.hex

def test_HexTypesAfterReset(tmpdir):
    """Reset board changes the HexTypes"""
    X = (4,5)

    assert tmpdir.board.getNodeDict()[X].getHexType() == HexGameRules.empty.hex

    tmpdir.board.makeMove(1,X)
    assert tmpdir.board.getNodeDict()[X].getHexType() == HexGameRules.blue.hex

    tmpdir.board.resetGameBoard()
    assert tmpdir.board.getNodeDict()[X].getHexType() == HexGameRules.empty.hex

def test_HexPlayerInfo(tmpdir):
    """Get each players info and check that it is correct"""

    blueInfo = HexGameRules.getPlayerInfo(1)
    assert blueInfo.player == 1
    assert blueInfo.start == (5,-1)
    assert blueInfo.end == (5,11)

    redInfo = HexGameRules.getPlayerInfo(2)
    assert redInfo.player == 2
    assert redInfo.start == (-1,5)
    assert redInfo.end == (11,5)

    assert HexGameRules.getPlayerHex(1) == HexGameRules.blue.hex
    assert HexGameRules.getPlayerHex(2) == HexGameRules.red.hex