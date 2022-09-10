from typing import Callable

from hexBoy.hex.board.HexBoard import HexBoard
from hexBoy.hex.node.HexNode import Hex

def SyncBoard(board: HexBoard, parentBoard: HexBoard, moveCallback: Callable[[Hex], None]=None):
    """Sync the current board to the parent board based on move history"""
    parentMoveLen: int = len(parentBoard.getMoveHistory())
    selfMoveLen: int = len(board.getMoveHistory())

    for i in range(selfMoveLen, parentMoveLen):
        player, move = parentBoard.getMoveHistory()[i]
        board.makeMove(player, move)

        if moveCallback != None:
            moveCallback(player, move)
