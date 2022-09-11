import pytest

from hexBoy.AI.GetAgent import GetAgent
from hexBoy.hex.game.HexGame import HexGame

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.game = HexGame(
        agent1=GetAgent(1),
        agent2=GetAgent(1),
    )

    # ^^^ before ^^^
    yield  # run the rest
    # vvv After vvv

def test_PlayGame(tmpdir):
    """Play a game and check that one of the agents one"""
    tmpdir.game.main()
    assert len(tmpdir.game._winPath) != 0
    assert tmpdir.game._currentGameNumber == 1
    assert (tmpdir.game._redWins + tmpdir.game._blueWins) == 1

def test_PlayMultipleGames(tmpdir):
    """Play a few games"""
    num = 5
    tmpdir.game.main(num)
    assert len(tmpdir.game._winPath) != 0
    assert tmpdir.game._currentGameNumber == num
    assert (tmpdir.game._redWins + tmpdir.game._blueWins) == num

def test_CheckTurns(tmpdir):
    """Check that turns change"""
    assert tmpdir.game._currentPlayer == 1
    tmpdir.game._switchTurns()
    assert tmpdir.game._currentPlayer == 2
    tmpdir.game._switchTurns()
    assert tmpdir.game._currentPlayer == 1

def test_MakeGameMove(tmpdir):
    """Make a game move and see it show up in the game"""
    assert tmpdir.game._gameBoard.validateMove((0, 0))
    tmpdir.game._handleNextMove(1, (0, 0))
    assert not tmpdir.game._gameBoard.validateMove((0, 0))

def test_GetAgentMove(tmpdir):
    """Agents should pick a move and do it. then check the board"""
    tmpdir.game._handleAgentTurn()
    assert tmpdir.game._nextMove != None
    tmpdir.game._handleNextMove(tmpdir.game._currentPlayer, tmpdir.game._nextMove)
    assert not tmpdir.game._gameBoard.validateMove(tmpdir.game._nextMove)
