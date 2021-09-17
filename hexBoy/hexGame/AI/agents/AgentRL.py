import random

from hexGame.pathfinder.PathBoy import PathBoy
from hexGame.HexBoard import Board
from hexGame.AI.HexAgent import HexAgent
from hexGame.HexNode import HexNode
from hexGame.AI.agentUtil.BoardEval import BoardStates
from hexGame.AI.agentUtil.MoveEval import evaluateMove
from hexGame.SortedDict import SortedDict

'''
-----------------------------------------------
Reinforcement Learning Agent
-----------------------------------------------
'''
class AgentRL(HexAgent):

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


  def __init__(self):
    HexAgent.__init__(self)
    self.name = "Agent_RL"
    self.transitionDict = {}

  def getAgentMove(self):
    currentState = self._getCurrentBoardState()

    # score last move
    if (self.stateBeforeLastMove):
      transition = (self.stateBeforeLastMove, self.stateAfterLastMove)

      # score transition
      self.transitionDict[transition] = self._scoreTransition(transition) 

    self.stateBeforeLastMove = currentState

    # (B1) get next move.
    # - get the best transition
    # - do one of the moves to that transition
    bestTransition = _getBestTransitionForDepth(1)

    self.stateAfterLastMove = bestNextState
    if (len(movesToConsider > 0)):
      # randomly pick a move that leads to the best state
      return random.choice(movesToConsider)
    else:
      # pick a random move if no moves were found
      return self._randomMove()

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
    return
    # reset states

  '''
  -----------------------------------------------
  Private
  -----------------------------------------------
  '''
  def _getCurrentBoardState(self):
    return [0,0,0,0]

  def _scoreTransition(self, transition):
    return 1

  def _getPossibleNextStates(self):
    return []

  def _getBestState(self, possibleStates):
    return [0,0,0,0]

  def _getPossibleMovesToState(bestNextState):
    return []

  def _getBestNextStateAndPossibleMoves(self):


  def _getBestTransitionForDepth(self, depth):
    def sortFunc(item): # sort by transition score
      return item[1]

    checkedTransitions = SortedDict(getSortValue = sortFunc, reverse = True)

    # recursion func to call
    def _bestTransitionRecursion(depth, board):
      nonlocal checkedTransitions

      # basecase
      if (depth == 0):
        stateAtDepth = _getStateFromBoard(board)
        transition = (initialState, stateAtDepth)
        # Score Transaction
        if (not checkedTransitions.hasKey(transition)):
          if (self.transitions.hasKey(transition)):
            self.transitions[transition] = self.initialTransitionValue
          checkedTransitions[transition] = self.transitions[transition]
        return

      # loop through possible moves from board
      possibleMoves = board.getPossibleMoves()
      for move in possibleMoves:
        nextBoard = board.getBoardFromMove(move)
        _bestTransitionRecursion(depth - 1, nextBoard)
      # end recursion func

    _bestTransitionRecursion(depth, self.board)
    bestTransition = checkedTransitions.pop() # pop off the best transition
    return bestTransition
