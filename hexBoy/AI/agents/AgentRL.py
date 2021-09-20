import random

from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.HexBoard import Board
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.HexNode import HexNode
from hexBoy.AI.agentUtil.BoardEval import BoardStates
from hexBoy.AI.agentUtil.MoveEval import evaluateMove
from hexBoy.SortedDict import SortedDict

'''
-----------------------------------------------
Reinforcement Learning Agent
-----------------------------------------------
'''
class AgentRL(HexAgent):

  # TODO make this into an object so its not ugly
  # board states: [
  #   Dp: playerDistToWin,
  #   Do: opponentDistToWin,
  #   Np: playerNumPaths,
  #   No: opponentNumPaths,
  # ]
  stateBeforeLastMove = None
  stateAfterLastMove = None
  transitionDict = None

  initialTransitionValue = 10 # value to set on first visit to transition

  ALPHA = 0.3 # learning rate
  LAMBDA = 0.1

  def __init__(self):
    HexAgent.__init__(self)
    self.name = "Agent_RL"
    self.transitionDict = SortedDict()

  def getAgentMove(self):
    currentState = self._getStateFromBoard(self.gameBoard)

    # score last move
    if (self.stateBeforeLastMove):
      transition = (self.stateBeforeLastMove, self.stateAfterLastMove)

      # update transition
      self.transitionDict[transition] = self._updateTransition(transition)

    self.stateBeforeLastMove = currentState

    # (B1) get next move.
    # - get the best transition
    # - do one of the moves to that transition
    bestTransition = self._getBestTransitionForDepth(1)
    movesToConsider = self._getPossibleMovesToState(bestTransition[1])

    if (len(movesToConsider) > 0):
      self.stateAfterLastMove = bestTransition[1]
      # randomly pick a move that leads to the best state
      return random.choice(movesToConsider)
    else:
      randomMove = self._randomMove()
      randomBoard = self.gameBoard.getBoardFromMove(randomMove, self.player)
      randomState = self._getStateFromBoard(randomBoard)
      self.stateAfterLastMove = randomState

      # pick a random move if no moves were found
      return randomMove

  def setGameBoardAndPlayer(self, gameBoard, player):
    HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

    # AStar Pathfinder
    def sortFunc(item):
      return item[1].g

    self.pathfinder = PathBoy(
      self.getAdjacentSpaces,
      1, #AStar
      sortFunc
    )

  def scoreGame(self):
    # reset states
    self.stateBeforeLastMove = None
    self.stateAfterLastMove = None

  '''
  -----------------------------------------------
  Private
  -----------------------------------------------
  '''
  def _rewardStateTransition(self, transition):

    gamma = 0.1
    theta = 1

    stateA = transition[0]
    stateB = transition[1]

    return (
      # gamma * (
      #   (stateB[2] - stateA[2])
      #   - (stateB[3] - stateB[3])
      # ) -
      100 -
      theta * (
        (stateB[0] - stateA[0])
        - (stateB[1] - stateA[1])
      )
    )

  def _getStateFromBoard(self, board):
    # board states: [
    #   Dp: playerDistToWin,
    #   Do: opponentDistToWin,
    #   Np: playerNumPaths,
    #   No: opponentNumPaths,
    # ]
    pf = self.pathfinder

    playerBestPath = pf.findPath(
      board.getNodeDict(),
      self.startPos,
      self.endPos,
      self.checkIfBarrier,
      HexNode.getCellValueForNextMove
    )
    Dp = pf.ScorePath(
      board.getNodeDict(),
      playerBestPath,
      HexNode.getCellValueForNextMove
    )
    opponentBestPath = pf.findPath(
      board.getNodeDict(),
      self.opponentStart,
      self.opponentEnd,
      self.checkIfOpponentBarrier,
      HexNode.getCellValueForNextMove
    )
    Do = pf.ScorePath(
      board.getNodeDict(),
      opponentBestPath,
      HexNode.getCellValueForNextMove
    )

    # Np = pf.NumBestPaths(
    #   board.getNodeDict(),
    #   self.startPos, self.endPos,
    #   self.checkIfBarrier,
    #   HexNode.getCellValueForNextMove
    # )
    # No = pf.NumBestPaths(
    #   board.getNodeDict(),
    #   self.opponentStart, self.opponentEnd,
    #   self.checkIfOpponentBarrier,
    #   HexNode.getCellValueForNextMove
    # )

    return (Dp, Do)

  def _getPossibleMovesToState(self, state):
    possibleMoves = []

    allMoves = self.gameBoard.getPossibleMoves()
    for move in allMoves:
      nextBoard = self.gameBoard.getBoardFromMove(move, self.player)
      nextState = self._getStateFromBoard(nextBoard)
      if (nextState == state):
        possibleMoves.append(move)

    return possibleMoves

  def _getBestTransitionForDepth(self, depth):
    # get the best transition from depth
    # Note: returned transition will have a value in self.transitions
    def sortFunc(item): # sort by transition score
      return item[1]

    checkedTransitions = SortedDict(getSortValue = sortFunc, reverse = False)
    initialState = self._getStateFromBoard(self.gameBoard)

    # recursion func to call
    def _bestTransitionRecursion(depth, board, player):
      nonlocal checkedTransitions

      # basecase
      if (depth == 0):
        stateAtDepth = self._getStateFromBoard(board)
        transition = (initialState, stateAtDepth)
        # Score Transaction
        if (not checkedTransitions.hasKey(transition)):
          if (not self.transitionDict.hasKey(transition)):
            self.transitionDict[transition] = self.initialTransitionValue
          checkedTransitions[transition] = self.transitionDict[transition]
        return

      # loop through possible moves from board
      possibleMoves = board.getPossibleMoves()
      for move in possibleMoves:
        nextBoard = board.getBoardFromMove(move, player)

        if (player == 1):
          nextPlayer = 2
        else:
          nextPlayer = 1

        _bestTransitionRecursion(depth - 1, nextBoard, nextPlayer)
      # end recursion func

    _bestTransitionRecursion(depth, self.gameBoard, self.player)
    bestTransitionTuple = checkedTransitions.popItem() # pop off the best transition

    return bestTransitionTuple[0]

  def _updateTransition(self, transition):
    # T(Sn, Sn1) <- T(Sn, Sn1)
    #   + alpha(
    #       R(Sn,Sn2)
    #     + lamba(maxM(T(Sn+2,Sm))
    #     - T(Sn, Sn1)
    #   )

    maxTransition = self._getBestTransitionForDepth(1)
    maxMVal = self.transitionDict[maxTransition]
    currentTransitionVal = self.transitionDict[transition]

    return (
      currentTransitionVal
      + self.ALPHA * (
        self._rewardStateTransition(transition)
        + self.LAMBDA * maxMVal
        - currentTransitionVal
      )
    )
