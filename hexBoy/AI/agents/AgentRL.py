import random
from dataclasses import dataclass
from tokenize import Double

from hexBoy.pathfinder.PathBoy import PathBoy
from hexBoy.hex.board.HexBoard import Board
from hexBoy.hex.node.HexNode import HexNode
from hexBoy.AI.HexAgent import HexAgent
from hexBoy.AI.agentUtil.agentRL.BoardEval import BoardStates
from hexBoy.AI.agentUtil.eval.MoveEval import evaluateMove
from hexBoy.models.SortedDict import SortedDict
from hexBoy.AI.agentUtil.agentRL.agentRLUtil import GetBoardFromMove, GetPossibleMoves
from hexBoy.hex.game.HexGameRules import HexGameRules

# TODO Come back later. I almost want to leave this class for a bit. Not close enough to do good RL.
'''----------------------------------
Reinforcement Learning Agent
----------------------------------'''
@dataclass
class AgentRL(HexAgent):
    # board states: (
    #   Dp: playerDistToWin,
    #   Do: opponentDistToWin,
    #   Np: playerNumPaths,
    #   No: opponentNumPaths,
    # )
    stateBeforeLastMove = None
    stateAfterLastMove = None
    transitionDict = None

    _pf: PathBoy
    _opf: PathBoy

    initialTransitionValue: int = 10  # value to set on first visit to transition

    ALPHA: Double = 0.3  # learning rate
    LAMBDA: Double = 0.1

    def __init__(self):
        HexAgent.__init__(self, "Agent_RL")
        self.transitionDict = SortedDict()
        self.initialTransitionValue = 10

    # Override
    def getAgentMove(self):
        currentState = self._getStateFromBoard(self._gameBoard)

        # score last move
        if self.stateBeforeLastMove:
            transition = (self.stateBeforeLastMove, self.stateAfterLastMove)

            # update transition
            self.transitionDict[transition] = self._updateTransition(transition)

        self.stateBeforeLastMove = currentState

        # (B1) get next move.
        # - get the best transition
        # - do one of the moves to that transition
        bestTransition = self._getBestTransitionForDepth(1)
        movesToConsider = self._getPossibleMovesToState(bestTransition[1])

        if len(movesToConsider) > 0:
            self.stateAfterLastMove = bestTransition[1]
            # randomly pick a move that leads to the best state
            return random.choice(movesToConsider)
        else:
            randomMove = self._randomMove()
            randomBoard = GetBoardFromMove(self._gameBoard, randomMove, self._playerInfo.player)
            randomState = self._getStateFromBoard(randomBoard)
            self.stateAfterLastMove = randomState

            # pick a random move if no moves were found
            return randomMove

    # Override
    def setGameBoardAndPlayer(self, gameBoard, player):
        HexAgent.setGameBoardAndPlayer(self, gameBoard, player)

        def sortFunc(item):
            return item[1].getPC()

        self._pf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._playerInfo.player), 
            HexGameRules.getHeuristicFunc(self._playerInfo.player), 
            sortFunc
        )

        self._opf = PathBoy(
            self._gameBoard, 
            HexGameRules.getCheckIfBarrierFunc(self._opponentInfo.player), 
            HexGameRules.getHeuristicFunc(self._opponentInfo.player), 
            sortFunc
        )

    def updateBoard(self):
        pass

    def scoreGame(self):
        # reset states
        self.stateBeforeLastMove = None
        self.stateAfterLastMove = None

    '''---
    Private
    ---'''
    def _rewardStateTransition(self, transition):

        gamma = 0.1
        theta = 1

        stateA = transition[0]
        stateB = transition[1]

        return (
            # gamma * (
            #   (stateB[2] - stateA[2])
            #   - (stateB[3] - stateB[3])
            # )
            100
            - theta * ((stateB[0] - stateA[0]) - (stateB[1] - stateA[1]))
        )

    def _getStateFromBoard(self, board):
        # board states: [
        #   Dp: playerDistToWin,
        #   Do: opponentDistToWin,
        #   Np: playerNumPaths,
        #   No: opponentNumPaths,
        # ]

        ppf = self._pf
        opf = self._opf

        Dp = ppf.findAndScorePath(
            self._playerInfo.start,
            self._playerInfo.end,
        )
        Do = opf.findAndScorePath(
            self._opponentInfo.start,
            self._opponentInfo.end,
        )

        # Np = pf.NumBestPaths(
        #   board.getNodeDict(),
        #   self.startPos, self.endPos,
        #   self.checkIfBarrier,
        # )

        # No = pf.NumBestPaths(
        #   board.getNodeDict(),
        #   self.opponentStart, self.opponentEnd,
        #   self.checkIfOpponentBarrier,
        # )

        return (Dp, Do)

    def _getPossibleMovesToState(self, state):
        possibleMoves = []

        allMoves = GetPossibleMoves(self._gameBoard)
        for move in allMoves:
            nextBoard = GetBoardFromMove(self._gameBoard, move, self._playerInfo.player)
            nextState = self._getStateFromBoard(nextBoard)
            if nextState == state:
                possibleMoves.append(move)

        return possibleMoves

    def _getBestTransitionForDepth(self, depth):
        # get the best transition from depth
        # Note: returned transition will have a value in self.transitions
        def sortFunc(item):  # sort by transition score
            return item[1]

        checkedTransitions = SortedDict(getSortValue=sortFunc, reverse=False)
        initialState = self._getStateFromBoard(self._gameBoard)

        # recursion func to call
        def _bestTransitionRecursion(depth, board, player):
            nonlocal checkedTransitions

            # base case
            if depth == 0:
                stateAtDepth = self._getStateFromBoard(board)
                transition = (initialState, stateAtDepth)
                # Score Transaction
                if not checkedTransitions.hasKey(transition):
                    if not self.transitionDict.hasKey(transition):
                        self.transitionDict[transition] = self.initialTransitionValue
                    checkedTransitions[transition] = self.transitionDict[transition]
                return

            # loop through possible moves from board
            possibleMoves = GetPossibleMoves(board)
            for move in possibleMoves:
                nextBoard = GetBoardFromMove(board, move, player)

                if player == 1:
                    nextPlayer = 2
                else:
                    nextPlayer = 1

                _bestTransitionRecursion(depth - 1, nextBoard, nextPlayer)
            # end recursion func

        _bestTransitionRecursion(depth, self._gameBoard, self._playerInfo.player)
        bestTransitionTuple = (
            checkedTransitions.popItem()
        )  # pop off the best transition

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

        return currentTransitionVal + self.ALPHA * (
            self._rewardStateTransition(transition)
            + self.LAMBDA * maxMVal
            - currentTransitionVal
        )
