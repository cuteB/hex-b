# NOTE Didn't really look at this file recently. Probs old
"""Probs remove"""
class BoardStates:

  bigBoardDict = None # dictionary of all
  player = None
  ALPHA = 0.1
  REWARD = 1
  GAMMA = 0.01


  def __init__(self, player):
    self.bigBoardDict = {}
    self.player = player

  def evaluateBoard(self, moveList):
    key = self._moveListToBoardKey(moveList)
    return self.bigBoardDict.get(key, 0)

  # TODO doing every move only do my moves
  def scoreBoardWin(self, board):
    moveList = board.moveHistory
    playerMoves = board.getPlayerMoves(self.player)

    i = 0
    key = self._moveListToBoardKey(moveList)
    oldValue = self.bigBoardDict.get(key, 0)

    y = self.GAMMA ** i
    newValue = oldValue + (self.ALPHA * (y * oldValue + self.REWARD))
    self.bigBoardDict[key] = newValue

    length = len(playerMoves)
    while (len(moveList) >= 2):
      i += 1
      moveList.pop()
      moveList.pop()
      key = self._moveListToBoardKey(moveList)
      oldValue = self.bigBoardDict.get(key, 0)

      y = self.GAMMA ** i
      newValue = oldValue + (self.ALPHA * (y * oldValue + self.REWARD))

      self.bigBoardDict[key] = newValue

  def scoreBoardLoss(self, board):
    moveList = board.moveHistory
    playerMoves = board.getPlayerMoves(self.player)
    length = len(moveList)
    moveList.pop()
    i = 0

    key = self._moveListToBoardKey(moveList)
    oldValue = self.bigBoardDict.get(key, 0)

    y = self.GAMMA ** (i / length)
    newValue = oldValue + (self.ALPHA * (y * oldValue - self.REWARD))

    self.bigBoardDict[key] = newValue

    while (len(moveList) >= 2):
      i += 1

      moveList.pop()
      moveList.pop()
      key = self._moveListToBoardKey(moveList)
      oldValue = self.bigBoardDict.get(key, 0)

      y = self.GAMMA ** (i / length)
      newValue = oldValue + (self.ALPHA * (y * oldValue - self.REWARD))

      self.bigBoardDict[key] = newValue

  def _moveListToBoardKey(self, moveList):
    OXNumbers = ['1', '2','3','4','5','6','8','9','a','b','c','d','e','f']
    key = ""

    def sortMoveFunc(moveCoord):
      return moveCoord[0] * 100 + moveCoord[1]

    moveList.sort(key=sortMoveFunc, reverse=True)

    for move in moveList:
      (x, y) = move
      key += str(OXNumbers[x]) + str(OXNumbers[y])

    return key

  def _sortMoveList(self, moveList):
    def sortMoveFunc(moveCoord):
      return moveCoord[0] * 100 + moveCoord[1]

    moveList.sort(key=sortMoveFunc, reverse=True)

    return moveList
