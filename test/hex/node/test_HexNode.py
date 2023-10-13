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

    X = HexNode((5,5))
    assert X == (5, 5)
    assert X[0] == 5
    assert X[1] == 5

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

def test_BestGet(tmpdir):
    """Test the get function for best"""

    assert tmpdir.X.getBest() == 1

    tmpdir.X.setPath(1)
    assert tmpdir.X.getBest() == 2

    tmpdir.X.setDist(1)
    assert tmpdir.X.getBest() == 3

def test_HeurGetSet(tmpdir):
    """Test the get and set functions for heur"""

    assert tmpdir.X.getHeur() == 0

    tmpdir.X.setHeur(5)
    assert tmpdir.X.getHeur() == 5

def test_HestGet(tmpdir):
    """Test the get function for Hest"""

    assert tmpdir.X.getHest() == 1

    tmpdir.X.setPath(1)
    assert tmpdir.X.getHest() == 2

    tmpdir.X.setHeur(1)
    assert tmpdir.X.getHest() == 3

def test_InitHexTypeNode(tmpdir):
    """Init HexNode with HexType in one line"""
    
    X = HexNode(tmpdir.X).initHexType(tmpdir.testHexType)
    xType = X.getHexType()
    assert xType.player == tmpdir.testHexType.player
    assert xType.cost == tmpdir.testHexType.cost
    assert xType.xType == tmpdir.testHexType.xType

# test dads
def test_DadGetSet(tmpdir):
    """Test the get and set functions for dad"""

    assert tmpdir.X.getDad() == None

    tmpdir.X.setDad(tmpdir.end)
    assert tmpdir.X.getDad() == tmpdir.end

def test_DadAdd(tmpdir):
    """Test the add function for dad"""

    tmpdir.X.addDad(tmpdir.end)
    assert tmpdir.X.getDad() == tmpdir.end

def test_DadDel(tmpdir):
    """Test the del function for dad"""

    tmpdir.X.addDad(tmpdir.end)
    assert tmpdir.X.getDad() == tmpdir.end

    tmpdir.X.delDad(tmpdir.end)
    assert tmpdir.X.getDad() == None

def test_getDads(tmpdir):
    """Test the get function for dads"""

    assert tmpdir.X.getDads() == []

    tmpdir.X.addDad(tmpdir.end)
    assert tmpdir.X.getDads() == [tmpdir.end]

# test sons
def test_SonGetSet(tmpdir):
    """Test the get and set functions for son"""

    assert tmpdir.X.getSon() == None

    tmpdir.X.setSon(tmpdir.end)
    assert tmpdir.X.getSon() == tmpdir.end

def test_SonAdd(tmpdir):
    """Test the add function for son"""

    tmpdir.X.addSon(tmpdir.end)
    assert tmpdir.X.getSon() == tmpdir.end

def test_SonDel(tmpdir):
    """Test the del function for son"""

    tmpdir.X.addSon(tmpdir.end)
    assert tmpdir.X.getSon() == tmpdir.end

    tmpdir.X.delSon(tmpdir.end)
    assert tmpdir.X.getSon() == None

def test_getSons(tmpdir):
    """Test the get function for sons"""

    assert tmpdir.X.getSons() == []

    tmpdir.X.addSon(tmpdir.end)
    assert tmpdir.X.getSons() == [tmpdir.end]

# test pathsToNode
def test_PathsToNodeGetSet(tmpdir):
    """Test the get and set functions for pathsToNode"""

    assert tmpdir.X.getPathsToNode() == 0

    tmpdir.X.setPathsToNode(5)
    assert tmpdir.X.getPathsToNode() == 5

def test_UpdatePathsToNodeWithDads(tmpdir):
    """Test the update function for pathsToNode with dads"""

    assert tmpdir.X.getPathsToNode() == 0

    dad1 = HexNode((1, 1))
    dad1.setPathsToNode(1)

    dad2 = HexNode((2, 2))
    dad2.setPathsToNode(2)

    tmpdir.X.addDad(dad1)
    tmpdir.X.updatePathsToNodeWithDads()
    assert tmpdir.X.getPathsToNode() == 1

    tmpdir.X.addDad(dad2)
    tmpdir.X.updatePathsToNodeWithDads()
    assert tmpdir.X.getPathsToNode() == 3

    tmpdir.X.delDad(dad1)
    tmpdir.X.updatePathsToNodeWithDads()
    assert tmpdir.X.getPathsToNode() == 2

def test_UpdatePathsFromNodesWithSons(tmpdir):
    """Test the update function for pathsFromNode with sons"""

    assert tmpdir.X.getPathsFromNode() == 0

    son1 = HexNode((1, 1))
    son1.setPathsFromNode(1)

    son2 = HexNode((2, 2))
    son2.setPathsFromNode(2)

    tmpdir.X.addSon(son1)
    tmpdir.X.updatePathsFromNodeWithSons()
    assert tmpdir.X.getPathsFromNode() == 1

    tmpdir.X.addSon(son2)
    tmpdir.X.updatePathsFromNodeWithSons()
    assert tmpdir.X.getPathsFromNode() == 3

    tmpdir.X.delSon(son1)
    tmpdir.X.updatePathsFromNodeWithSons()
    assert tmpdir.X.getPathsFromNode() == 2
