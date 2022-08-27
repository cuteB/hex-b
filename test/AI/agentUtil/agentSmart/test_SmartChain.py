import pytest

from hexBoy.hex.HexBoard import Board
from hexBoy.AI.agentUtil.agentSmart.SmartChain import SmartChain

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""

    tmpdir.board = Board()

    # ^^^ before ^^^
    yield # run the rest
    # vvv after vvv

def test_EmptyBoardChain(tmpdir):
    """Empty Board"""
    
    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = None
    assert actual == expected

    # end
    actual = chain.endPos
    expected = None
    assert actual == expected

    # length
    actual = chain.length
    expected = 0
    assert actual == expected

    # connections
    actual = chain.connections
    expected = []
    assert set(actual) == set(expected)

   # start dist
    actual = chain.startDist
    expected = None
    assert actual == expected

    # end dist
    actual = chain.endDist
    expected = None
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert actual == expected

def test_EmptyBoardChainWithOppMove(tmpdir):
    """Empty Board but with opp move"""
    
    tmpdir.board.makeMove((5,5), 2)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = None
    assert actual == expected

    # end
    actual = chain.endPos
    expected = None
    assert actual == expected

    # length
    actual = chain.length
    expected = 0
    assert actual == expected

    # connections
    actual = chain.connections
    expected = []
    assert set(actual) == set(expected)

   # start dist
    actual = chain.startDist
    expected = None
    assert actual == expected

    # end dist
    actual = chain.endDist
    expected = None
    assert actual == expected
    
    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert set(actual) == set(expected)

def test_SingleHexChain(tmpdir):
    """Single hex in the chain"""
    
    tmpdir.board.makeMove((5,5), 1)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (5,5)
    assert actual == expected

    # length
    actual = chain.length
    expected = 1
    assert actual == expected

    # connections
    actual = chain.connections
    expected = []
    assert set(actual) == set(expected)

    
   # start dist
    actual = chain.startDist
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.endDist
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

    tmpdir.board.makeMove((5,5), 1)

    chain.updateChain()

    # start
    actual = chain.startPos
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (5,5)
    assert actual == expected

    # length
    actual = chain.length
    expected = 1
    assert actual == expected

    # connections
    actual = chain.connections
    expected = []
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.endDist
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

    tmpdir.board.makeMove((5,5), 2)

    # start
    actual = chain.startPos
    expected = None
    assert actual == expected

    # end
    actual = chain.endPos
    expected = None
    assert actual == expected

    # length
    actual = chain.length
    expected = 0
    assert actual == expected

    # connections
    actual = chain.connections
    expected = []
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = None
    assert actual == expected

    # end dist
    actual = chain.endDist
    expected = None
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert set(actual) == set(expected)

def test_TwoHexChain(tmpdir):
    """Board with two hexes touching"""

    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,6), 1)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (5,6)
    assert actual == expected

    # length
    actual = chain.length
    expected = 2
    assert actual == expected

    # connections
    actual = chain.connections
    expected = []
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.endDist
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

    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((5,7), 1)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (5,7)
    assert actual == expected

    # length
    actual = chain.length
    expected = 3
    assert actual == expected

    # connections
    actual = chain.connections
    expected = [(5,6)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.endDist
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

    tmpdir.board.makeMove((5,5), 1)
    tmpdir.board.makeMove((4,7), 1)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (4,7)
    assert actual == expected

    # length
    actual = chain.length
    expected = 3 
    assert actual == expected

    # connections
    actual = chain.connections
    expected = [(4,6), (5,6)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 5
    assert actual == expected

    # end dist
    actual = chain.endDist
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

    tmpdir.board.makeMove((5,1), 1)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (5,1)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (5,1)
    assert actual == expected

    # length
    actual = chain.length
    expected = 2
    assert actual == expected

    # connections
    actual = chain.connections
    expected = [(5,0), (6,0)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 1
    assert actual == expected

    # end dist
    actual = chain.endDist
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
        tmpdir.board.makeMove((5,i), 1)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (5,0)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (5,10)
    assert actual == expected

    # length
    actual = chain.length
    expected = 11
    assert actual == expected

    # connections
    actual = chain.connections
    expected = []
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 0
    assert actual == expected

    # end dist
    actual = chain.endDist
    expected = 0
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert set(actual) == set(expected)

def test_ThreeStrongHexChain(tmpdir):
    """Board with three hexes with strong connections"""

    moves = [(5,4), (4,6), (3,8)]
    for m in moves:
        tmpdir.board.makeMove(m,1)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (5,4)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (3,8)
    assert actual == expected

    # length
    actual = chain.length
    expected = 5
    assert actual == expected

    # connections
    actual = chain.connections
    expected = [(3,7), (4,5), (4,7), (5,5)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 4
    assert actual == expected

    # end dist
    actual = chain.endDist
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
        tmpdir.board.makeMove(m,1)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (8,1)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (4,9)
    assert actual == expected

    # length
    actual = chain.length
    expected = 11
    assert actual == expected

    # connections
    actual = chain.connections
    expected = [(8,0), (9,0), (7,2), (8,2), (6,4), (7,4), (5,6), (6,6), (4,8), (5,8), (3,10), (4,10)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 1
    assert actual == expected

    # end dist
    actual = chain.endDist
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
        tmpdir.board.makeMove(m,2)

    chain = SmartChain(2, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (1,7)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (9,3)
    assert actual == expected

    # length
    actual = chain.length
    expected = 11
    assert actual == expected

    # connections
    actual = chain.connections
    expected = [(0,7), (0,8), (2,6), (2,7), (4,5), (4,6), (6,4), (6,5), (8,3), (8,4), (10,2), (10,3)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 1
    assert actual == expected

    # end dist
    actual = chain.endDist
    expected = 1
    assert actual == expected

    # potential moves
    actual = chain.getPotentialMoves()
    expected = []
    assert set(actual) == set(expected)

def test_RedTwoStrongHexChain(tmpdir):
    """Red Board with two hexes in a strong connection""" 

    tmpdir.board.makeMove((5,5), 2)
    tmpdir.board.makeMove((3,6), 2)

    chain = SmartChain(2, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (3,6)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (5,5)
    assert actual == expected

    # length
    actual = chain.length
    expected = 3 
    assert actual == expected

    # connections
    actual = chain.connections
    expected = [(4,5), (4,6)]
    assert set(actual) == set(expected)
    
   # start dist
    actual = chain.startDist
    expected = 3
    assert actual == expected

    # end dist
    actual = chain.endDist
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
    