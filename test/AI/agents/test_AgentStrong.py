import pytest

from hexBoy.AI.agents.AgentStrong import AgentStrong
from hexBoy.AI.agents.AgentRand import AgentRand
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.game.HexGame import HexGame

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.board = HexBoard()
    tmpdir.agent = AgentStrong()
    tmpdir.agent.setGameBoardAndPlayer(tmpdir.board, 1)

    # ^^^ before ^^^
    yield  # run the rest
    # vvv After vvv

def test_AgentStrongMakesValidMove(tmpdir):
    """Get a move from the agent and validate the move on the board"""
    move = tmpdir.agent.getAgentMove()
    assert tmpdir.board.validateMove(move)

def test_AgentStrongFullGame(tmpdir):
    """Test full game with the agent playing both sides"""
    game = HexGame(
        agent1=AgentStrong(),
        agent2=AgentRand(),
    )

    assert game.main() == True

