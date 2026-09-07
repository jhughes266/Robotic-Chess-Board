import math
import time
from chess_adversarial_search.game import Game
import chess

def timeBoundedMinimaxAlphaBetaSearch(game, chessBoard, maxSearchTimeSeconds, maxSearchPlyDepth):
    """
    Perform an iterative deepening search. Estimates how long the next ply will take based on the time ratios between
    previous plys. Once the estimate for the next ply is greater than the max search time the search terminates
    Args:
          game: Game object that contains a representation of the chess game.
          chessBoard: chess board object.
          maxSearchTimeSeconds: The maximum search time in seconds.
          maxSearchPlyDepth: The maximum search ply depth. If the search is shorter than the max search time then once it
          reaches the maxSearchPlyDepth it will terminate otherwise it reverts to the maximum search time.
    Returns:
        The best move according to the minimax alpha beta search algorithm.
    """
    searchStartTime = time.perf_counter()
    # Stores the search times of different plys
    plySearchTimes = []
    move = None
    currentPlyDepth = 1

    while True:
        plyStartTime = time.perf_counter()
        # perform the minimaxAlphaBetaSearch
        move = minimaxAlphaBetaSearch(game, chessBoard, currentPlyDepth)
        plyEndTime = time.perf_counter()
        currentPlyTime = plyEndTime - plyStartTime
        # Append the search time for the current ply to the list
        plySearchTimes.append(currentPlyTime)

        # Will always evaluate to at least 2 ply depth. This allows proper calculation of time increase factors between
        # plys.
        if currentPlyDepth > 1:
            timeIncreaseFactor = 0
            # Loop through all the ply search times.
            for i in range(1, len(plySearchTimes)):
                # Calculate the time increase factors between consecutive plys and sum these
                timeIncreaseFactor += (plySearchTimes[i] / plySearchTimes[i-1])
            # Get the average time increase factor between plys
            averageTimeIncreaseFactor = timeIncreaseFactor / (len(plySearchTimes) - 1)
            # Get the projected search time for the next ply
            projectedSearchTimeAfterNextPly = (time.perf_counter() - searchStartTime) + (averageTimeIncreaseFactor * currentPlyTime)
            # Cease the search once the maximum time has been exceeded or the max search depth has been reached.
            if (projectedSearchTimeAfterNextPly > maxSearchTimeSeconds) or (currentPlyDepth==maxSearchPlyDepth):
                # Print information on the search.
                print(f"\n---------------------------------------\nSearched to a depth of {currentPlyDepth}.\nThe time spent on searching the final ply was {round(currentPlyTime, 4)} seconds. \nThe average time increase factor between plys is {round(averageTimeIncreaseFactor, 4)}.\nThe total search time was {round(time.perf_counter() - searchStartTime, 4)} seconds.\n---------------------------------------\n")
                # Break out of the search loop
                break
        # Increment the current ply depth that is being searched to.
        currentPlyDepth += 1
    # Return the move that has been found.
    return move

def minimaxAlphaBetaSearch(game, chessBoard, maxPlyDepth):
    """
    Determines the player and then uses either the max(white) or min function to begin search execution.
    Args:
         chessBoard: A python chess board object.
         maxPlyDepth: The maximum ply depth of the search.
    Returns:
        The move found by the minimax alpha beta search algorithm.
    """
    player = game.toMove(chessBoard)
    move = None
    if player == chess.WHITE:
        value, move = maxValue(game=game, chessBoard=chessBoard, alpha=-math.inf, beta=math.inf, plyDepth=0, maxPlyDepth=maxPlyDepth)
    elif player == chess.BLACK:
        value, move = minValue(game=game, chessBoard=chessBoard, alpha=-math.inf, beta=math.inf, plyDepth=0, maxPlyDepth=maxPlyDepth)

    return move

def maxValue(game, chessBoard, alpha, beta, plyDepth, maxPlyDepth):
    """
    Finds a move that will maximize the utility of the white player.
    Args:
        game: Game object that contains a representation of the chess game.
        chessBoard: A python chess board object.
        alpha: The best utility available to max
    Returns:
        bestValue: The best utility found so far
        bestMove: The move corresponding to the bestValue
    """
    # Check if the game is terminal and if it is calculate the utility
    if game.isTerminal(chessBoard):
        return game.utility(chessBoard, plyDepth), None
    # Terminate the search if the search is at the maximum ply depth and perform evaluation of the current board state
    elif plyDepth == maxPlyDepth:
        return game.evaluate(chessBoard), None
    # The best value max has found so far. Is initially negative infinity (ie: as bad as possible for max)
    bestValue = -math.inf
    bestMove = None
    # Obtain all the actions available.
    availableMoves = game.actions(chessBoard)
    # Loop through all the available moves
    for move in availableMoves:
        # Call min function as this simulates the black players move. Pass the alpha and beta values down the tree. This
        # way future branches can be pruned.
        candidateValue, _ = minValue(game=game, chessBoard=game.result(chessBoard, move), alpha=alpha, beta=beta, plyDepth=plyDepth+1, maxPlyDepth=maxPlyDepth)
        # Update the best value if the candidate value is better than the best value.
        if candidateValue > bestValue:
            bestValue = candidateValue
            bestMove = move
            # Update alpha if the best value is greater than alpha.
            alpha = max(bestValue, alpha)
        # Reverse the move by removing it from the move stack. This can be done because we are essentially performing a
        # depth first search which is conducive with a stacks behaviour.
        game.reverseMove(chessBoard)
        # Beta represent a value that can be obtained by min in a prior branch of the tree. If the best max value is
        # greater then it we dont need to search any further because we know that min will take that route because if it
        # went down this path then max would get a better score.
        if bestValue >= beta:
            return bestValue, bestMove

    return bestValue, bestMove


def minValue(game, chessBoard, alpha, beta, plyDepth, maxPlyDepth):
    """
    Opposite of max refer to max for documentation and comments
    """
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
