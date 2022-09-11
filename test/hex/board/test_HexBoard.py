import pytest

from hexBoy.hex.board.HexBoard import HexBoard

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board before each test"""
    tmpdir.board = HexBoard()

    # ^^^ before ^^^
    yield # run the rest
    # vvv After vvv

def test_BoardBounds(tmpdir):
    """Test Bounds of the Board"""
    assert tmpdir.board.isSpaceWithinBounds((0,0))
    assert tmpdir.board.isSpaceWithinBounds((-1,0))
    assert tmpdir.board.isSpaceWithinBounds((0,11))
    assert tmpdir.board.isSpaceWithinBounds((5,5))
    assert not tmpdir.board.isSpaceWithinBounds((-1,-1))
    assert not tmpdir.board.isSpaceWithinBounds((11,11))

def test_AdjacentSpacesBasic(tmpdir):
    """Check Adjacent Spaces the board, make sure they are on the board"""
    space = (1,1)
    actual = tmpdir.board.getAdjacentSpaces(space)
    expected = [(1,0), (1,2), (0,1), (2,1), (0,2), (2,0)]
    assert actual == expected

def test_AdjacentSpacesEdge(tmpdir):
    """Check Adjacent Spaces of edge"""
    space = (-1,0)
    actual = tmpdir.board.getAdjacentSpaces(space)
    expected = [(-1,1), (0,0), (0,-1)]
    assert actual == expected

def test_AdjacentSpacesOfPlayerMove(tmpdir):
    """Check Adjacent Spaces the board with player moves"""
    space = (1,1)
    tmpdir.board.makeMove(1,space)
    actual = tmpdir.board.getAdjacentSpaces(space)
    expected = [(1,0), (1,2), (0,1), (2,1), (0,2), (2,0)]
    assert actual == expected

def test_AdjacentSpacesWithAllTakenMoves(tmpdir):
    """Check Adjacent Spaces when all spaces are taken"""
    space = (1,1)
    tmpdir.board.makeMove(1,space)
    tmpdir.board.makeMove(1,(1,0))
    tmpdir.board.makeMove(2,(1,2))
    tmpdir.board.makeMove(1,(0,1))
    tmpdir.board.makeMove(2,(2,1))
    tmpdir.board.makeMove(1,(0,2))
    tmpdir.board.makeMove(2,(2,0))
    actual = tmpdir.board.getAdjacentSpaces(space)
    expected = [(1,0), (1,2), (0,1), (2,1), (0,2), (2,0)]
    assert actual == expected

def test_ValidateAndMakeMove(tmpdir):
    """Validate and make moves, check that previous move is invalid"""

    move = (0,0)
    assert tmpdir.board.validateMove(move)
    tmpdir.board.makeMove(1, move)
    assert not tmpdir.board.validateMove(move)

    badMove = (-1, -1)
    assert not tmpdir.board.validateMove(badMove)

def test_ResetBoard(tmpdir):
    """Reset the board to all empty"""

    move = (0,0)
    tmpdir.board.makeMove(1, move)
    assert not tmpdir.board.validateMove(move)
    tmpdir.board.resetGameBoard()
    assert tmpdir.board.validateMove(move)

def test_validateEdges(tmpdir):
    """edges are valid"""

    assert  not tmpdir.board.validateMove((4,11))

def test_GetPlayerEndZone(tmpdir):
    """Get the player end zones"""

    actualBlueEndZone = tmpdir.board.getPlayerEndZone(1)
    actualRedEndZone = tmpdir.board.getPlayerEndZone(2)

    expectedBlueEndZone = [
        (0, -1), (0, 11), 
        (1, -1), (1, 11), 
        (2, -1), (2, 11), 
        (3, -1), (3, 11), 
        (4, -1), (4, 11), 
        (5, -1), (5, 11), 
        (6, -1), (6, 11), 
        (7, -1), (7, 11), 
        (8, -1), (8, 11), 
        (9, -1), (9, 11), 
        (10, -1), (10, 11)
    ] 

    expectedRedEndZone = [
        (-1, 0), (11, 0), 
        (-1, 1), (11, 1), 
        (-1, 2), (11, 2), 
        (-1, 3), (11, 3), 
        (-1, 4), (11, 4), 
        (-1, 5), (11, 5), 
        (-1, 6), (11, 6), 
        (-1, 7), (11, 7), 
        (-1, 8), (11, 8), 
        (-1, 9), (11, 9), 
        (-1, 10), (11, 10)
    ]

    assert  set(actualBlueEndZone) == set(expectedBlueEndZone)
    assert  set(actualRedEndZone) == set(expectedRedEndZone)
