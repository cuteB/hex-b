from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import pytest

from hexBoy.hex.game.HexGame import HexGame
from hexBoy.AI.GetAgent import GetAgent

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
  """Reset the board and pathfinder before each test"""
  tmpdir.game = HexGame(
    computer1=GetAgent(1),
    computer2=GetAgent(1),
  )

  # ^^^ before ^^^
  yield # run the rest
  # vvv After vvv

def test_PlayGame(tmpdir):
  """Play a game and check that one of the agents one"""
  tmpdir.game.main()
  assert len(tmpdir.game.winPath) != 0
  assert tmpdir.game.gameNumber == 1
  assert (tmpdir.game.redWins + tmpdir.game.blueWins) == 1

def test_PlayMultipleGames(tmpdir):
  """Play a few games"""
  num = 5
  tmpdir.game.main(num)
  assert len(tmpdir.game.winPath) != 0
  assert tmpdir.game.gameNumber == num
  assert (tmpdir.game.redWins + tmpdir.game.blueWins) == num

def test_CheckTurns(tmpdir):
  """Check that turns change"""
  assert tmpdir.game.player == 1
  tmpdir.game._switchTurns()
  assert tmpdir.game.player == 2
  tmpdir.game._switchTurns()
  assert tmpdir.game.player == 1

def test_MakeGameMove(tmpdir):
  """Make a game move and see it show up in the game"""
  assert tmpdir.game.board.validateMove((0,0))
  tmpdir.game.handleNextMove((0,0), 1)
  assert not tmpdir.game.board.validateMove((0,0))

def test_GetAgentMove(tmpdir):
  """Agents should pick a move and do it. then check the board"""
  tmpdir.game.handleAgentTurn()
  assert tmpdir.game.nextMove != None
  tmpdir.game.handleNextMove(tmpdir.game.nextMove, tmpdir.game.player)
  assert not tmpdir.game.board.validateMove(tmpdir.game.nextMove)
