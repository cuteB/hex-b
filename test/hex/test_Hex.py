import pytest

from hexBoy.hex.HexNode import Hex, HexNode, DefaultHexType, HexType

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

def test_HexNodeInit(tmpdir):
  """Does HexNode the inherit Hex"""
  X = HexNode(tmpdir.X)
  assert X == (5,5)
  assert X[0] == 5
  assert X[1] == 5
  assert X.x == 5
  assert X.y == 5

def test_DefaultHexTypeNode(tmpdir):
  """Does HexNode the inherit Hex"""
  X = HexNode(tmpdir.X)
  assert X.xType.player == DefaultHexType.player
  assert X.xType.cost == DefaultHexType.cost
  assert X.xType.hexType == DefaultHexType.hexType
