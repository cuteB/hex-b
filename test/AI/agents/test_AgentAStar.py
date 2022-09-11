import pytest

from hexBoy.AI.agents.AgentAStar import AgentAStar
from hexBoy.AI.agents.AgentRand import AgentRand
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.game.HexGame import HexGame

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.board = HexBoard()
    tmpdir.agent = AgentAStar()
    tmpdir.agent.setGameBoardAndPlayer(tmpdir.board, 1)

    # ^^^ before ^^^
    yield  # run the rest
    # vvv After vvv

def test_AgentAStarMakesValidMove(tmpdir):
    """Get a move from the agent and validate the move on the board"""
    move = tmpdir.agent.getAgentMove()
    assert tmpdir.board.validateMove(move)

def test_AgentAStarFullGame(tmpdir):
    """Test full game with the agent playing both sides"""
    game = HexGame(
        agent1=AgentAStar(),
        agent2=AgentRand(),
    )

    assert game.main() == True
