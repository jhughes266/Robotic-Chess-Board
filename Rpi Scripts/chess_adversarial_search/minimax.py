import math

from chess_adversarial_search.game import Game
import chess

def minimaxSearch(game, chessBoard):
    player = game.toMove(chessBoard)
    if player == chess.WHITE:
        value, move = maxValue(game, chessBoard, plyDepth=0)
    elif player == chess.BLACK:
        value, move = minValue(game, chessBoard, plyDepth=0)

    return move

def maxValue(game, chessBoard, plyDepth):
    if game.isTerminal(chessBoard, plyDepth):
        return game.utility(chessBoard), None

    bestValue = -math.inf
    bestMove = None

    availableMoves = game.actions(chessBoard)

    for move in availableMoves:
        candidateValue, _ = minValue(game, game.result(chessBoard, move), plyDepth=plyDepth+1)
        if candidateValue > bestValue:
            bestValue = candidateValue
            bestMove = move

        game.reverseMove(chessBoard)

    return bestValue, bestMove


def minValue(game, chessBoard, plyDepth):
    if game.isTerminal(chessBoard, plyDepth):
        return game.utility(chessBoard), None

    bestValue = math.inf
    bestMove = None

    availableMoves = game.actions(chessBoard)

    for move in availableMoves:
        candidateValue, _ = maxValue(game, game.result(chessBoard, move), plyDepth=plyDepth+1)

        if candidateValue < bestValue:
            bestValue = candidateValue
            bestMove = move

        game.reverseMove(chessBoard)

    return bestValue, bestMove
