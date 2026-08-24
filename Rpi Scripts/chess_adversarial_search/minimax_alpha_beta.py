import math
import time
from chess_adversarial_search.game import Game
import chess

def timeBoundedMinimaxAlphaBetaSearch(game, chessBoard, maxSearchTimeSeconds, maxSearchPlyDepth):
    searchStartTime = time.perf_counter()
    plySearchTimes = []
    move = None
    currentPlyDepth = 1

    while True:
        plyStartTime = time.perf_counter()
        move = minimaxAlphaBetaSearch(game, chessBoard, currentPlyDepth)
        plyEndTime = time.perf_counter()
        currentPlyTime = plyEndTime - plyStartTime
        plySearchTimes.append(currentPlyTime)

        if currentPlyDepth > 1:
            timeIncreaseFactor = 0
            for i in range(1, len(plySearchTimes)):
                timeIncreaseFactor += (plySearchTimes[i] / plySearchTimes[i-1])
            averageTimeIncreaseFactor = timeIncreaseFactor / (len(plySearchTimes) - 1)

            projectedSearchTimeAfterNextPly = (time.perf_counter() - searchStartTime) + (averageTimeIncreaseFactor * currentPlyTime)

            if (projectedSearchTimeAfterNextPly > maxSearchTimeSeconds) or (currentPlyDepth==maxSearchPlyDepth):
                """
                print(f"\n---------------------------------------\nSearched to a depth of {currentPlyDepth}.\nThe time spent on searching the final ply was {round(currentPlyTime, 4)} seconds. \nThe average time increase factor between plys is {round(averageTimeIncreaseFactor, 4)}.\nThe total search time was {round(time.perf_counter() - searchStartTime, 4)} seconds.\n---------------------------------------\n")
                """

                break

        currentPlyDepth += 1


    return move

def minimaxAlphaBetaSearch(game, chessBoard, maxPlyDepth):
    player = game.toMove(chessBoard)
    move = None
    if player == chess.WHITE:
        value, move = maxValue(game=game, chessBoard=chessBoard, alpha=-math.inf, beta=math.inf, plyDepth=0, maxPlyDepth=maxPlyDepth)
    elif player == chess.BLACK:
        value, move = minValue(game=game, chessBoard=chessBoard, alpha=-math.inf, beta=math.inf, plyDepth=0, maxPlyDepth=maxPlyDepth)

    return move

def maxValue(game, chessBoard, alpha, beta, plyDepth, maxPlyDepth):
    if game.isTerminal(chessBoard):
        return game.utility(chessBoard, plyDepth), None
    elif plyDepth == maxPlyDepth:
        return game.evaluate(chessBoard), None

    bestValue = -math.inf
    bestMove = None

    availableMoves = game.actions(chessBoard)

    for move in availableMoves:
        candidateValue, _ = minValue(game=game, chessBoard=game.result(chessBoard, move), alpha=alpha, beta=beta, plyDepth=plyDepth+1, maxPlyDepth=maxPlyDepth)
        if candidateValue > bestValue:
            bestValue = candidateValue
            bestMove = move
            alpha = max(bestValue, alpha)

        game.reverseMove(chessBoard)

        if bestValue >= beta:
            return bestValue, bestMove

    return bestValue, bestMove


def minValue(game, chessBoard, alpha, beta, plyDepth, maxPlyDepth):
    if game.isTerminal(chessBoard):
        return game.utility(chessBoard, plyDepth), None
    elif plyDepth == maxPlyDepth:
        return game.evaluate(chessBoard), None

    bestValue = math.inf
    bestMove = None

    availableMoves = game.actions(chessBoard)

    for move in availableMoves:
        candidateValue, _ = maxValue(game=game, chessBoard=game.result(chessBoard, move), alpha=alpha, beta=beta, plyDepth=plyDepth+1, maxPlyDepth=maxPlyDepth)

        if candidateValue < bestValue:
            bestValue = candidateValue
            bestMove = move
            beta = min(bestValue, beta)

        game.reverseMove(chessBoard)

        if bestValue <= alpha:
            return bestValue, bestMove

    return bestValue, bestMove
