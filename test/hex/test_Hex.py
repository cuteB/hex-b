import pytest

from hexBoy.hex.HexNode import Hex

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
  """Reset the board and pathfinder before each test"""
  tmpdir.X = Hex((5,5))


  # ^^^ before ^^^
  yield # run the rest
  # vvv After vvv

def test_HexValues(tmpdir):
  """Does the Hex work like a tuple"""
  assert tmpdir.X == (5,5)
  assert tmpdir.X[0] == 5
  assert tmpdir.X[1] == 5
  assert tmpdir.X.x == 5
  assert tmpdir.X.y == 5

