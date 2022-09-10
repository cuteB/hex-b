from hexBoy.hex.node.HexNode import Hex

def TrimEdgesFromPath(path: Hex): 
    """Trim the edges from the path"""
    trimmed = []
    for X in path:
        if (
            X[0] != -1 and X[0] != 11
            and X[1] != -1 and X[1] != 11
        ):
            trimmed.append(X)

    return trimmed