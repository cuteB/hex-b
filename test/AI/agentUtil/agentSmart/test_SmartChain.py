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

    # TODO start, end distances

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

def test_TwoStrongHexChain(tmpdir):
    """Board with two hexes touching"""

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

def test_ChainTouchingEndzone(tmpdir):
    """Board with two hexes touching"""

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

def test_CompletedChain(tmpdir):
    """Board with two hexes touching"""

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

def test_ThreeStrongHexChain(tmpdir):
    """Board with two hexes touching"""

    moves = [(5,5), (4,7), (3,9)]
    for m in moves:
        tmpdir.board.makeMove(m,1)

    chain = SmartChain(1, tmpdir.board)

    # start
    actual = chain.startPos
    expected = (5,5)
    assert actual == expected

    # end
    actual = chain.endPos
    expected = (3,9)
    assert actual == expected

    # length
    actual = chain.length
    expected = 5
    assert actual == expected

    # connections
    actual = chain.connections
    expected = [(3,8), (4,6), (4,8), (5,6)]
    assert set(actual) == set(expected)

