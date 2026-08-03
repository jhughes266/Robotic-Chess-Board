import math

from chess_adversarial_search.game import Game
import chess

def minimaxAlphaBetaSearch(game, chessBoard, maxPlyDepth):
    player = game.toMove(chessBoard)
    if player == chess.WHITE:
        value, move = maxValue(game=game, chessBoard=chessBoard, alpha=-math.inf, beta=math.inf, plyDepth=0, maxPlyDepth=maxPlyDepth)
    elif player == chess.BLACK:
        value, move = minValue(game=game, chessBoard=chessBoard, alpha=-math.inf, beta=math.inf, plyDepth=0, maxPlyDepth=maxPlyDepth)

    return move

def maxValue(game, chessBoard, alpha, beta, plyDepth, maxPlyDepth):
    if game.isTerminal(chessBoard):
        return game.utility(chessBoard), None
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
        return game.utility(chessBoard), None
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
