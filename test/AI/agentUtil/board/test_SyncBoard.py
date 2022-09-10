import pytest

from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.node.HexNode import Hex
from hexBoy.AI.agentUtil.board.SyncBoard import SyncBoard

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.gameBoard = HexBoard()
    tmpdir.agentBoard = HexBoard()

    # ^^^ before ^^^
    yield  # run the rest
    # vvv After vvv

def test_SyncOneMoveBoard(tmpdir):
    """Get a move from the agent and validate the move on the board"""
    move: Hex = (5,5)
    tmpdir.gameBoard.makeMove(1,move)

    assert tmpdir.agentBoard.validateMove(move) == True

    SyncBoard(tmpdir.agentBoard, tmpdir.gameBoard)
    assert tmpdir.agentBoard.validateMove(move) == False
