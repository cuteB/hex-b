import pytest

from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.node.HexNode import HexNode
from hexBoy.pathfinder.NumPathFinder import NumPathFinder

@pytest.fixture(autouse=True)
def before_and_after_test(tmpdir):
    """Reset the board and pathfinder before each test"""

    tmpdir.board = HexBoard()
    tmpdir.npf = NumPathFinder(tmpdir.board, 1)
    tmpdir.npf.initEmptyBoard()
    
    # ^^^ before ^^^
    yield # run the rest
    # vvv after vvv

def test_EmptySmartBoardNodePCDMiddle(tmpdir):
    """Nodes have PCD and family set"""

    # middle
    X: HexNode = tmpdir.board.getNodeDict()[(5,5)]
    assert X.getPath() == 5
    assert X.getDist() == 5
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(5,4), (6,4)])
    assert set(X.getSons()) == set([(4,6), (5,6)])

    # short edge 
    X = tmpdir.board.getNodeDict()[(10,3)]
    assert X.getPath() == 3
    assert X.getDist() == 7
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(10,2)])
    assert set(X.getSons()) == set([(9,4), (10,4)])

    # long edge
    X = tmpdir.board.getNodeDict()[(0,1)]
    assert X.getPath() == 1
    assert X.getDist() == 9
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(0,0), (1,0)])
    assert set(X.getSons()) == set([(0,2)])

    # start edge
    X = tmpdir.board.getNodeDict()[(2,0)]
    assert X.getPath() == 0
    assert X.getDist() == 10
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(2,-1)])
    assert set(X.getSons()) == set([(1,1), (2,1)])

    # end edge
    X = tmpdir.board.getNodeDict()[(4,10)]
    assert X.getPath() == 10
    assert X.getDist() == 0
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(4,9), (5,9)])
    assert set(X.getSons()) == set([(4,11)])

    # start end zone
    X = tmpdir.board.getNodeDict()[(5, -1)]
    assert set(X.getDads()) == set([])
    assert set(X.getSons()) == set([(5,0)])

    # end end zone
    X = tmpdir.board.getNodeDict()[(5, 11)]
    assert set(X.getDads()) == set([(5,10)])
    assert set(X.getSons()) == set([])

def test_MoreEmptySmartBoardNodePCDMiddle(tmpdir):
    """Testing more nodes, Some nodes might be acting funny"""

    X: HexNode = tmpdir.board.getNodeDict()[(6,6)]
    assert X.getPath() == 6
    assert X.getDist() == 4
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(6,5), (7,5)])
    assert set(X.getSons()) == set([(5,7), (6,7)])

    X = tmpdir.board.getNodeDict()[(3,6)]
    assert X.getPath() == 6
    assert X.getDist() == 4
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(3,5), (4,5)])
    assert set(X.getSons()) == set([(2,7), (3,7)])

    X = tmpdir.board.getNodeDict()[(10,-1)]
    assert X.getPath() == 0
    assert X.getDist() == 11
    assert X.getBest() == 11
    assert set(X.getDads()) == set([])
    assert set(X.getSons()) == set([(10,0)])

    X = tmpdir.board.getNodeDict()[(5,11)]
    assert X.getPath() == 11
    assert X.getDist() == 0
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(5,10)])
    assert set(X.getSons()) == set([])

def test_EmptySmartBoardTotalPaths(tmpdir):
    """Empty board paths for a player"""

    assert tmpdir.npf.getNumPaths() == 6144
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((5,5)) == 32

    assert tmpdir.npf.getNumPathsToHex((0, 10)) == 1024
    assert tmpdir.npf.getNumPathsToHex((1, 10)) == 1023
    assert tmpdir.npf.getNumPathsToHex((2, 10)) == 1013
    assert tmpdir.npf.getNumPathsToHex((3, 10)) == 968
    assert tmpdir.npf.getNumPathsToHex((4, 10)) == 848
    assert tmpdir.npf.getNumPathsToHex((5, 10)) == 638
    assert tmpdir.npf.getNumPathsToHex((6, 10)) == 386
    assert tmpdir.npf.getNumPathsToHex((7, 10)) == 176
    assert tmpdir.npf.getNumPathsToHex((8, 10)) == 56
    assert tmpdir.npf.getNumPathsToHex((9, 10)) == 11
    assert tmpdir.npf.getNumPathsToHex((10, 10)) == 1
    

def test_SmartBoardWithMiddleMove(tmpdir):
    """Board with the move in the middle"""

    tmpdir.board.makeMove(1, (5,5))
    tmpdir.npf.updateMove(1, (5,5))

    assert tmpdir.npf.getNumPaths() == 1024
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((5,5)) == 32

def test_NodeValuesAfterOnePlayerMove(tmpdir):
    """Values not in the best path should still be updated"""

    moves = [(5,5)]
    for m in moves:
        tmpdir.board.makeMove(1, m)
        tmpdir.npf.updateMove(1, m)
    
    X = tmpdir.board.getNodeDict()[(4,5)]
    
    assert X.getPath() == 5
    assert X.getDist() == 5
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(4,4), (5,4), (5,5)])
    assert set(X.getSons()) == set([(3,6), (4,6), (5,5)])

    X = tmpdir.board.getNodeDict()[(6,5)]
    
    assert X.getPath() == 5
    assert X.getDist() == 5
    assert X.getBest() == 11
    assert set(X.getDads()) == set([(6,4), (7,4), (5,5)])
    assert set(X.getSons()) == set([(5,6), (6,6), (5,5)])

def test_NodeValuesAfterTwoPlayerMoves(tmpdir):
    """Values not in the best path should still be updated after two moves"""

    moves = [(3,6), (2,7)]
    for m in moves:
        tmpdir.board.makeMove(1, m)
        tmpdir.npf.updateMove(1, m)
    
    X = tmpdir.board.getNodeDict()[(2,6)]
    
    assert X.getPath() == 6
    assert X.getDist() == 3
    assert X.getBest() == 10
    assert (set(X.getDads()) == set([(2,5), (3,5), (2,7)])
        or  set(X.getDads()) == set([(2,5), (3,5), (3,6)]))
    assert (set(X.getSons()) == set([(3,7)])
        or set(X.getSons()) == set([(2,7)]))

def test_SmartBoardWithMiddleOppMove(tmpdir):
    """Board with the opp move inn the middle"""

    tmpdir.board.makeMove(2, (5,5))
    tmpdir.npf.updateMove(2, (5,5))

    assert tmpdir.npf.getNumPaths() == 5120

def test_SmartBoardWithTwoMoves(tmpdir):
    """Board with two strong moves"""

    moves = [(5,5), (4,7)]
    for m in moves:
        tmpdir.board.makeMove(1, m)
        tmpdir.npf.updateMove(1, m)

    assert tmpdir.npf.getNumPaths() == 512
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((4,7)) == 8

def test_SmartBoardWithThreeMoves(tmpdir):
    """Board with three strong moves"""

    moves = [(5,5), (4,7), (3,9)]
    for m in moves:
        tmpdir.board.makeMove(1, m)
        tmpdir.npf.updateMove(1, m)
    
    assert tmpdir.npf.getNumPaths() == 256
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((3,9)) == 2

def test_ConnectingClustersWithThreeMoves(tmpdir):
    """Board that connects two moves into a single cluster"""

    moves = [(5,5), (4,7), (4,6)]
    for m in moves:
        tmpdir.board.makeMove(1, m)
        tmpdir.npf.updateMove(1, m)
    
    assert tmpdir.npf.getNumPaths() == 256
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((4,7)) == 8

def test_SmartBoardWithThreeMovesUpdateDad(tmpdir):
    """Board with three strong moves in a different place"""

    moves = [(5,5), (4,7), (6,3)]
    for m in moves:
        tmpdir.board.makeMove(1, m)
        tmpdir.npf.updateMove(1, m)
    
    assert tmpdir.npf.getNumPaths() == 256
    assert tmpdir.npf.getNumPathsToHex((6,3)) == 8
    assert tmpdir.npf.getNumPathsFromHex((4,7)) == 8

def test_SmartBoardWithMoveAndOppMove(tmpdir):
    """One Move from Each Player"""
 
    tmpdir.board.makeMove(1, (5,5))
    tmpdir.npf.updateMove(1, (5,5))
    tmpdir.board.makeMove(2, (5,6))
    tmpdir.npf.updateMove(2, (5,6))

    assert tmpdir.npf.getNumPaths() == 512
    assert tmpdir.npf.getNumPathsToHex((5,5)) == 32
    assert tmpdir.npf.getNumPathsFromHex((5,5)) == 16

def test_SmartBoardWithScatteredMoves(tmpdir):
    """A bunch of moves from one player"""

    moves = [(10,0), (10,10), (5,5), (2,8), (5,6), (6,6)]
    numPaths = [1024, 1, 33, 4, 28, 36]
    pathsTo = [1, 1, 1, 1, 1, 1]
    pathsFrom = [1024, 1, 32, 4, 28, 36]

    for i in range(len(moves)):
        tmpdir.board.makeMove(1, moves[i])
        tmpdir.npf.updateMove(1, moves[i])

        assert tmpdir.npf.getNumPaths() == numPaths[i]
        assert tmpdir.npf.getNumPathsToHex(moves[i]) == pathsTo[i]
        assert tmpdir.npf.getNumPathsFromHex(moves[i]) == pathsFrom[i]

def test_NumPathsForBoardWithChain(tmpdir):
    """Make a chain and check start and end paths"""

    moves = [(5,5), (6,3)]
    start = [(5,5), (6,3)]
    end = [(5,5), (5,5)]

    numPaths = [1024, 512]
    startPaths = [32, 8]
    endPaths = [32, 32]

    for i in range(len(moves)):
        tmpdir.board.makeMove(1, moves[i])
        tmpdir.npf.updateMove(1, moves[i])

        assert tmpdir.npf.getNumPaths() == numPaths[i]
        assert tmpdir.npf.getNumPathsToHex(start[i]) == startPaths[i]
        assert tmpdir.npf.getNumPathsFromHex(end[i]) == endPaths[i]
        

def test_NumPathsEventuallyBlockingMoves(tmpdir):
    """Have opponent moves slowly change the path of the player"""
    
    m = (5,5)
    tmpdir.board.makeMove(1, m)
    tmpdir.npf.updateMove(1, m)

    assert tmpdir.npf.getNumPaths() == 1024
    assert tmpdir.npf.getNumPathsToHex(m) == 32
    assert tmpdir.npf.getNumPathsFromHex(m) == 32

    # opp moves
    oMoves = [(5,7), (4,6)]
    numPaths = [768, 256]
    startPaths = [32, 32]
    endPaths = [24, 8]

    for i in range(len(oMoves)):
        tmpdir.board.makeMove(2, oMoves[i])
        tmpdir.npf.updateMove(2, oMoves[i])

        assert tmpdir.npf.getNumPaths() == numPaths[i]
        assert tmpdir.npf.getNumPathsToHex(m) == startPaths[i]
        assert tmpdir.npf.getNumPathsFromHex(m) == endPaths[i]

def test_NumPathsEventuallySurroundingMove(tmpdir):
    """Have opponent moves surround a player move to force the path elsewhere"""
    
    m = (5,5)
    tmpdir.board.makeMove(1, m)
    tmpdir.npf.updateMove(1, m)

    assert tmpdir.npf.getNumPaths() == 1024
    assert tmpdir.npf.getNumPathsToHex(m) == 32
    assert tmpdir.npf.getNumPathsFromHex(m) == 32

    # opp moves
    oMoves = [(4,5), (6,5), (6,4), (5,6), (5,4), (4,6)]
    numPaths = [1024, 1024, 512, 256, 3136, 3136]
    startPaths = [32, 32, 16, 16, 32, 0]
    endPaths = [32, 32, 32, 16, 16, 0]

    for i in range(len(oMoves)):
        tmpdir.board.makeMove(2, oMoves[i])
        tmpdir.npf.updateMove(2, oMoves[i])

        assert tmpdir.npf.getNumPaths() == numPaths[i]
        assert tmpdir.npf.getNumPathsToHex(m) == startPaths[i]
        assert tmpdir.npf.getNumPathsFromHex(m) == endPaths[i]

def test_SampleGameTrackingBothPlayers(tmpdir):
    """Play a game and track the number of paths for each player"""

    pMoves = [(5,5), (3,6), (2,7), (0,9), (0,8), (0,7), (1,5), (1,9), (2,9), (2,3), (7,8), (8,6), (9,4), (10,2), (3,10), (4,8), (6,5), (8,4), (9,2), (10,1)]
    oMoves = [(5,6), (3,7), (2,8), (1,8), (1,7), (2,5), (0,10), (1,10), (2,10), (4,9), (5,7), (7,5), (8, 3), (9,1), (3,9), (5,8), (6,6), (7,4), (8,2), (10,0)]

    pNumPaths_a = [1024, 2432, 896, 128, 128, 128, 64, 64, 64, 32, 32, 32, 32, 64, 32, 32, 32, 32, 32, 32,32]  # Player moves after player move
    oNumPaths_a = [5120, 736, 256, 128, 128, 128, 128, 128, 64, 480, 80, 228, 40, 80, 108, 36, 15, 8, 3, 1]     # opp moves after player move
    pNumPaths_b = [512, 1152, 384, 128, 128, 96, 64, 64, 64, 32, 32, 32, 32, 64, 32, 32, 32, 32, 32, 0]      # Player moves after opp move
    oNumPaths_b = [992, 512, 256, 64, 64, 128, 64, 64, 480, 128, 320, 80, 140, 180, 72, 36, 15, 6, 2, 1]      # opp moves after opp move

    pBoard = HexBoard()
    pNPF = NumPathFinder(pBoard, 1)
    pNPF.initEmptyBoard()
    oBoard = HexBoard()
    oNPF = NumPathFinder(oBoard, 2)
    oNPF.initEmptyBoard()

    for i in range(len(pMoves)):
        # Player move for Player Board
        pBoard.makeMove(1, pMoves[i])
        pNPF.updateMove(1, pMoves[i])
        assert pNPF.getNumPaths() == pNumPaths_a[i]
        
        # Player move for Opp Board
        oBoard.makeMove(1, pMoves[i])
        oNPF.updateMove(1, pMoves[i])
        assert oNPF.getNumPaths() == oNumPaths_a[i]

        # Opp move for Player Board
        pBoard.makeMove(2, oMoves[i])
        pNPF.updateMove(2, oMoves[i])
        assert pNPF.getNumPaths() == pNumPaths_b[i]
        
        # Opp move for Opp Board
        oBoard.makeMove(2, oMoves[i])
        oNPF.updateMove(2, oMoves[i])
        assert oNPF.getNumPaths() == oNumPaths_b[i]
