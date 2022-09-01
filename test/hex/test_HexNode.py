import pytest

from hexBoy.hex.HexNode import HexNode

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
  """Reset the board and pathfinder before each test"""
  tmpdir.node = HexNode((0,0))
  tmpdir.end = (11,0)

  # ^^^ before ^^^
  yield # run the rest
  # vvv After vvv

def test_NodeValues(tmpdir):
  """Check default values for node"""
  assert tmpdir.node == (0,0)
  assert tmpdir.node.type == HexNode.SpaceTypes.EMPTY
  assert tmpdir.node.hest == 0

def test_ScoreNode(tmpdir):
  """Score node and check that it's cost and parent are set"""
  dad = (1,0)
  dadCost = 10
  tmpdir.node.scoreHeuristic(dad, dadCost, tmpdir.end)

  assert tmpdir.node.path == dadCost
  assert tmpdir.node.cost == 1
  assert tmpdir.node.getPC() == (dadCost + 1)
  assert tmpdir.node.parent == dad

def test_EmptyNodeBarrier(tmpdir):
  """Check that the empty node is a barrier for red and blue"""
  assert HexNode.checkIfBlueBarrier(tmpdir.node)
  assert HexNode.checkIfRedBarrier(tmpdir.node)

def test_EmptyNodeBarrierForAI(tmpdir):
  """Check that the empty node is not a barrier for red and blue for Agents"""
  assert not HexNode.checkIfBlueBarrierForAI(tmpdir.node)
  assert not HexNode.checkIfRedBarrierForAI(tmpdir.node)

def test_CheckIfEnd(tmpdir):
  """Check if the node is an end node for empty and end node"""
  endNode = HexNode(HexNode.SpaceTypes.RED_END, (5,5))
  assert not tmpdir.node.checkIfEnd()
  assert endNode.checkIfEnd()

def test_NodeColour(tmpdir):
  """Check the nodes colour for blue or not blue"""
  blue = HexNode(HexNode.SpaceTypes.BLUE, (0,0))
  blueEnd = HexNode(HexNode.SpaceTypes.BLUE_END, (0,0))
  blueEdge = HexNode(HexNode.SpaceTypes.BLUE_EDGE, (0,0))
  red = HexNode(HexNode.SpaceTypes.RED, (0,0))

  assert blue.checkIfBlue()
  assert blueEnd.checkIfBlue()
  assert blueEdge.checkIfBlue()
  assert not red.checkIfBlue()
  assert not tmpdir.node.checkIfBlue()

def test_ExtraPathsToNode(tmpdir):
  """Check functions that set and add extra paths"""
  assert tmpdir.node.extraPathsToThisNode == 0

  tmpdir.node.setExtraPathsToNode(5)
  assert tmpdir.node.extraPathsToThisNode == 5

  tmpdir.node.addExtraPathsToNode(3)
  assert tmpdir.node.extraPathsToThisNode == 8

