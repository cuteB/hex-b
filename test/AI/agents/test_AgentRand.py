import pytest

from hexBoy.AI.agents.AgentRand import AgentRand
from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.game.HexGame import HexGame, HexGameOptions

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.board = HexBoard()
    tmpdir.agent = AgentRand()
    tmpdir.agent.setGameBoardAndPlayer(tmpdir.board, 1)

    # ^^^ before ^^^
    yield  # run the rest
    # vvv After vvv

def test_AgentRandMakesValidMove(tmpdir):
    """Get a move from the agent and validate the move on the board"""
    move = tmpdir.agent.getAgentMove()
    assert tmpdir.board.validateMove(move)

def test_AgentRandFullGame(tmpdir):
    """Test full game with the agent playing both sides"""
    testOptions = HexGameOptions(gameType="test", testMode=True)
    game = HexGame(
        agent1=AgentRand(),
        agent2=AgentRand(),
        options=testOptions
    )

    assert game.main() == True
