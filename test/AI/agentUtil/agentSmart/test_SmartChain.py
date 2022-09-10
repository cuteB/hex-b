import pytest

from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.AI.agentUtil.agentSmart.SmartChain import SmartChain

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""

    tmpdir.board = HexBoard()

    # ^^^ before ^^^
    yield # run the rest
    # vvv after vvv

def test_EmptyBoardChain(tmpdir):
    """Empty Board"""
    
    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = None
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = None
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 0
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = []
    assert set(actual) == set(expected)

   # start dist
    actual = chain.getStartDist()
    expected = None
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = None
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert actual == expected

def test_EmptyBoardChainWithOppMove(tmpdir):
    """Empty Board but with opp move"""
    
    tmpdir.board.makeMove(2, (5,5))

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = None
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = None
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 0
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = []
    assert set(actual) == set(expected)

   # start dist
    actual = chain.getStartDist()
    expected = None
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = None
    assert actual == expected
    
    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert set(actual) == set(expected)

def test_SingleHexChain(tmpdir):
    """Single hex in the chain"""
    
    tmpdir.board.makeMove(1, (5,5))

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (5,5)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 1
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = []
    assert set(actual) == set(expected)

    
   # start dist
    actual = chain.getStartDist()
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 5
    assert actual == expected
    
    # potential moves
    actual = chain.getPotentialMoves()
    expected = [
        (6,3),
        (4,4), (5,4), (6,4), (7,4),
        (4,5), (6,5),
        (3,6), (4,6), (5,6), (6,6),
        (4,7)
    ]
    assert set(actual) == set(expected)

def test_SingleHexChainUpdate(tmpdir):
    """Single hex move after init, test update"""
    
    chain = SmartChain(1, tmpdir.board)

    tmpdir.board.makeMove(1, (5,5))

    chain.updateChain()

    # start
    actual = chain.getStartPos()
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (5,5)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 1
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = []
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 5
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = [
        (6,3),
        (4,4), (5,4), (6,4), (7,4),
        (4,5), (6,5),
        (3,6), (4,6), (5,6), (6,6),
        (4,7)
    ]
    assert set(actual) == set(expected)

def test_SingleOpponentHexChain(tmpdir):
    """Single Opponent Hex"""
    
    chain = SmartChain(1, tmpdir.board)

    tmpdir.board.makeMove(2, (5,5))

    # start
    actual = chain.getStartPos()
    expected = None
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = None
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 0
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = []
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = None
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = None
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert set(actual) == set(expected)

def test_TwoHexChain(tmpdir):
    """Board with two hexes touching"""

    tmpdir.board.makeMove(1, (5,5))
    tmpdir.board.makeMove(1, (5,6))

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (5,6)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 2
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = []
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 4
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = [
        (6,3),
        (4,4), (5,4), (6,4), (7,4),
        (4,5), (6,5),
        (4,6), (6,6),
        (3,7), (4,7), (5,7), (6,7),
        (4,8)
    ]
    assert set(actual) == set(expected)

def test_TwoHexWeakChain(tmpdir):
    """Board with two hexes connected by a weak connection"""

    tmpdir.board.makeMove(1, (5,5))
    tmpdir.board.makeMove(1, (5,7))

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (5,7)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 3
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = [(5,6)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 3
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = [
        (6,3),
        (4,4), (5,4), (6,4), (7,4),
        (4,5), (6,5),
        (4,6), (6,6),
        (4,7), (6,7),
        (3,8), (4,8), (5,8), (6,8),
        (4,9)
    ]
    assert set(actual) == set(expected)

def test_TwoStrongHexChain(tmpdir):
    """Board with two hexes in a strong connection"""

    tmpdir.board.makeMove(1, (5,5))
    tmpdir.board.makeMove(1, (4,7))

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (4,7)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 3 
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = [(4,6), (5,6)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 3
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = [
        (6,3),
        (4,4), (5,4), (6,4), (7,4),
        (4,5), (6,5),
        (3,7), (5,7),
        (2,8), (3,8), (4,8), (5,8),
        (3,9)
    ]
    assert set(actual) == set(expected)

def test_ChainTouchingEndZone(tmpdir):
    """Board with one move that has a strong connection to the end zone"""

    tmpdir.board.makeMove(1, (5,1))

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (5,1)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (5,1)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 2
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = [(5,0), (6,0)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 1
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 9
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = [
        (4,1), (6,1),
        (3,2), (4,2), (5,2), (6,2),
        (4,3),
 
    ]
    assert set(actual) == set(expected)

def test_CompletedChain(tmpdir):
    """Board with a completed path"""

    for i in range(11):
        tmpdir.board.makeMove(1, (5,i))

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (5,0)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (5,10)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 11
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = []
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 0
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 0
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert set(actual) == set(expected)

def test_ThreeStrongHexChain(tmpdir):
    """Board with three hexes with strong getConnections()"""

    moves = [(5,4), (4,6), (3,8)]
    for m in moves:
        tmpdir.board.makeMove(1, m)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (5,4)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (3,8)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 5
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = [(3,7), (4,5), (4,7), (5,5)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 4
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 2
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = [
        (6,2),
        (4,3), (5,3), (6,3), (7,3),
        (4,4), (6,4),
        (2,8), (4,8),
        (1,9), (2,9), (3,9), (4,9),
        (2,10)
    ]
    assert set(actual) == set(expected)

def test_FullStrongChain(tmpdir):
    """Board with a full chain of strongly connected dexes touching both player ends"""

    moves = [(8,1), (7,3), (6,5), (5,7), (4,9)]
    for m in moves:
        tmpdir.board.makeMove(1, m)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (8,1)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (4,9)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 11
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = [(8,0), (9,0), (7,2), (8,2), (6,4), (7,4), (5,6), (6,6), (4,8), (5,8), (3,10), (4,10)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 1
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 1
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert set(actual) == set(expected)

def test_RedFullStrongChain(tmpdir):
    """Red Board with a full chain of strongly connected dexes touching both player ends"""

    moves = [(5,5), (3,6), (7,4), (1,7), (9,3)]
    for m in moves:
        tmpdir.board.makeMove(2, m)

    chain = SmartChain(2, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (1,7)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (9,3)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 11
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = [(0,7), (0,8), (2,6), (2,7), (4,5), (4,6), (6,4), (6,5), (8,3), (8,4), (10,2), (10,3)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 1
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 1
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert set(actual) == set(expected)

def test_RedTwoStrongHexChain(tmpdir):
    """Red Board with two hexes in a strong connection""" 

    tmpdir.board.makeMove(2, (5,5))
    tmpdir.board.makeMove(2, (3,6))

    chain = SmartChain(2, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (3,6)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (5,5)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 3 
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = [(4,5), (4,6)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 3
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 5
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = [
        (1,7),
        (2,5), (2,6), (2,7), (2,8),
        (3,5), (3,7),
        (5,4), (5,6),
        (6,3), (6,4), (6,5), (6,6),
        (7,4)
    ]
    assert set(actual) == set(expected)
    
def test_BrokenChainBoard(tmpdir):
    """Ran into this state where the chain doesn't work""" 

    playerMoves = [(5,5), (4,5), (3,6), (5,4)]
    oppMoves =    [(5,6), (4,6), (9,6), (8,6)]

    for i in range(4):
        tmpdir.board.makeMove(1, playerMoves[i])
        tmpdir.board.makeMove(2, oppMoves[i])

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.getStartPos()
    expected = (5,4)
    assert actual == expected

    # end
    actual = chain.getEndPos()
    expected = (3,6)
    assert actual == expected

    # getLength()
    actual = chain.getLength()
    expected = 3
    assert actual == expected

    # getConnections()
    actual = chain.getConnections()
    expected = []
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.getStartDist()
    expected = 4
    assert actual == expected

    # end dist
    actual = chain.getEndDist()
    expected = 4
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = [
        (6,2),
        (4,3), (5,3), (6,3), (7,3),
        (4,4), (6,4),
        (2,6), (2,7), (3,5),
        (1,7), (2,7), (3,7),
        (2,8)
    ]
    assert set(actual) == set(expected)
    