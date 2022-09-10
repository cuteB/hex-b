from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.node.HexNode import Hex
from hexBoy.pathfinder.PathBoy import PathBoy

def GetDistanceToCenter(X: Hex) -> int:
    """Get distance to the center of a hex Board"""
    
    center: Hex = (5,5)
    board: HexBoard = HexBoard() # Always use blank board
    pf = PathBoy(board)

    path = pf.findPath(X,center)

    if (path[0] == X): # Should always be true
        path.remove(X)

    return len(path)
