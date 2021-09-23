import pytest
from hexBoy.AI.GetAgent import GetAgent
from hexBoy.hex.HexBoard import Board

# TODO write more tests for agents. Not sure what I should do with them

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
  """Reset the board and pathfinder before each test"""
  tmpdir.board = Board(11)
  tmpdir.agent = GetAgent()
  tmpdir.agent.setGameBoardAndPlayer(tmpdir.board, 1)

  # ^^^ before ^^^
  yield # run the rest
  # vvv After vvv

def test_AgentMakesValidMove(tmpdir):
  """Get a move from the agent and validate the move on the board"""
  move = tmpdir.agent.getAgentMove()
  assert tmpdir.board.validateMove(move)
