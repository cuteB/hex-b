import pytest

from hexBoy.AI.agents.AgentRL import AgentRL
# from hexBoy.AI.agents.AgentRand import AgentRand
from hexBoy.hex.board.HexBoard import HexBoard
# from hexBoy.hex.game.HexGame import HexGame

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.board = HexBoard()
    tmpdir.agent = AgentRL()
    tmpdir.agent.setGameBoardAndPlayer(tmpdir.board, 1)

    # ^^^ before ^^^
    yield  # run the rest
    # vvv After vvv

def test_AgentRLMakesValidMove(tmpdir):
    """Get a move from the agent and validate the move on the board"""
    move = tmpdir.agent.getAgentMove()
    assert tmpdir.board.validateMove(move)

# Really slow so skipping
# def test_AgentRLFullGame(tmpdir):
#     """Test full game with the agent playing both sides"""
#     game = HexGame(
#         agent1=AgentRL(),
#         agent2=AgentRand(), # using rand agent to speed things up
#     )

#     assert game.main() == True
