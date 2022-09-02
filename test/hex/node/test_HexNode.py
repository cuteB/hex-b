import pytest

from hexBoy.hex.node.HexNode import Hex, HexNode, HexType, DefaultHexType

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""
    tmpdir.X = HexNode((0, 0))
    tmpdir.testHexType = HexType(player=1, xType=5, cost=9)
    tmpdir.end = (11, 0)

    # ^^^ before ^^^
    yield  # run the rest
    # vvv After vvv

def test_HexNodeInit(tmpdir):
    """Does HexNode inherit Hex and tuple"""
    hex = Hex((5, 5))
    X = HexNode(hex)
    assert X == (5, 5)
    assert X[0] == 5
    assert X[1] == 5
    assert X.x == 5
    assert X.y == 5

    X = HexNode((5,5))
    assert X == (5, 5)
    assert X[0] == 5
    assert X[1] == 5
    assert X.x == 5
    assert X.y == 5

def test_DefaultHexTypeNode(tmpdir):
    """Does HexNode get the default HexType"""
    X = HexNode(tmpdir.X)
    xType = X.getHexType()
    assert xType.player == DefaultHexType.player
    assert xType.cost == DefaultHexType.cost
    assert xType.xType == DefaultHexType.xType

def test_SetHexType(tmpdir):
    """Set and Get Hex Type"""
    testHexType = tmpdir.testHexType
    tmpdir.X.setHexType(testHexType)

    xType = tmpdir.X.getHexType()
    assert xType.player == testHexType.player
    assert xType.xType == testHexType.xType
    assert xType.cost == testHexType.cost

def test_PathGetSet(tmpdir):
    """Test the get and set functions for path"""
    assert tmpdir.X.getPath() == 0

    tmpdir.X.setPath(5)
    assert tmpdir.X.getPath() == 5

def test_CostGetSet(tmpdir):
    """Test the get and set functions for cost"""
    assert tmpdir.X.getCost() == DefaultHexType.cost

    tmpdir.X.setHexType(tmpdir.testHexType)
    assert tmpdir.X.getCost() == tmpdir.testHexType.cost

def test_DistGetSet(tmpdir):
    """Test the get and set functions for dist"""
    assert tmpdir.X.getDist() == 0

    tmpdir.X.setDist(5)
    assert tmpdir.X.getDist() == 5

def test_BestGetSet(tmpdir):
    """Test the get and set functions for best"""
    assert tmpdir.X.getBest() == 0

    tmpdir.X.setBest(5)
    assert tmpdir.X.getBest() == 5

def test_HeurGetSet(tmpdir):
    """Test the get and set functions for heur"""
    assert tmpdir.X.getHeur() == 0

    tmpdir.X.setHeur(5)
    assert tmpdir.X.getHeur() == 5

def test_HestGetSet(tmpdir):
    """Test the get and set functions for dist"""
    assert tmpdir.X.getHest() == 0

    tmpdir.X.setHest(5)
    assert tmpdir.X.getHest() == 5
