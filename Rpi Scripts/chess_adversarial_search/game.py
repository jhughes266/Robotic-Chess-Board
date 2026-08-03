from unittest import result
import math
import random
import chess
from chess_adversarial_search.misc import Timer

class Game:

    def __init__(self):
        pass

    def toMove(self, chessBoard):
        return chessBoard.turn

    def actions(self, chessBoard):
        # May need to adapt this for the promotion if material is not available
        unorderedLegalMoves = list(chessBoard.legal_moves)
        # HERE IS WHERE PROMOTIONS WOULD BE FILTERED OUT
        
        captures = []
        threats = []
        forwardMoves = []
        remainingMoves = []

        if chessBoard.turn == chess.WHITE:
            for move in unorderedLegalMoves:
                originSquare = move.from_square
                destinationSquare = move.to_square

                # Check for captures
                destinationSquareBitMask = (1 << destinationSquare)
                occupiedByBlackBitMask = chessBoard.occupied_co[chess.BLACK]
                if occupiedByBlackBitMask & destinationSquareBitMask:
                    captures.append(move)
                    continue

                # Check for threats
                # A move is potentially mitigating a threat if the moves origin is being attacked. We can use the
                # attackers function to check for attackers from the origin square of the move. If there is any the
                # bit mask will contain 1's and be greater than 0 and evaluate true. If there is none it will equal 0.
                if int(chessBoard.attackers(chess.BLACK, originSquare)):
                    threats.append(move)
                    continue

                # Check for forward moves.
                originRank = chess.square_rank(originSquare)
                destinationRank = chess.square_rank(destinationSquare)
                if destinationRank >= originRank:
                    forwardMoves.append(move)
                    continue

                # Append remaining moves.
                remainingMoves.append(move)

        elif chessBoard.turn == chess.BLACK:
            for move in unorderedLegalMoves:
                originSquare = move.from_square
                destinationSquare = move.to_square

                # Check for captures
                destinationSquareBitMask = (1 << destinationSquare)
                occupiedByWhiteBitMask = chessBoard.occupied_co[chess.WHITE]
                if occupiedByWhiteBitMask & destinationSquareBitMask:
                    captures.append(move)
                    continue

                # Check for threats
                # A move is potentially mitigating a threat if the moves origin is being attacked. We can use the
                # attackers function to check for attackers from the origin square of the move. If there is any the
                # bit mask will contain 1's and be greater than 0 and evaluate true. If there is none it will equal 0.
                if int(chessBoard.attackers(chess.WHITE, originSquare)):
                    threats.append(move)
                    continue

                # Check for forward moves.
                originRank = chess.square_rank(originSquare)
                destinationRank = chess.square_rank(destinationSquare)
                if destinationRank <= originRank:
                    forwardMoves.append(move)
                    continue

                # Append remaining moves.
                remainingMoves.append(move)

        # Concat lists
        orderedLegalMoves = captures + threats + forwardMoves + remainingMoves
        #print(len(unorderedLegalMoves)==len(orderedLegalMoves))

        return orderedLegalMoves


    def result(self, chessBoard, move):
        chessBoard.push(move)
        return chessBoard

    def reverseMove(self, chessBoard):
        return chessBoard.pop()

    def isTerminal(self, chessBoard):
        ## This may need expanding ##
        return chessBoard.is_game_over()

    def utility(self, chessBoard):
        resultStr = chessBoard.result()
        # For the time being a draw is assigned a zero (this may need changing)
        if resultStr == '1/2-1/2':
            return 0
        # We now know that the score is either '1-0' or '0-1'
        elif resultStr == '1-0':
            # White wins
            return 99999
        elif resultStr == '0-1':
            # Black wins
            return -99999
        else:
            raise RuntimeError("Attempted to calculate utility but the game was not in a terminal state!")

    def evaluate(self, chessBoard):
        estimatedUtility = 0

        estimatedUtility += (chessBoard.pieces_mask(chess.PAWN, chess.WHITE).bit_count() * 1)
        estimatedUtility += (chessBoard.pieces_mask(chess.BISHOP, chess.WHITE).bit_count() * 3)
        estimatedUtility += (chessBoard.pieces_mask(chess.KNIGHT, chess.WHITE).bit_count() * 3)
        estimatedUtility += (chessBoard.pieces_mask(chess.ROOK, chess.WHITE).bit_count() * 5)
        estimatedUtility += (chessBoard.pieces_mask(chess.QUEEN, chess.WHITE).bit_count() * 9)

        estimatedUtility += (chessBoard.pieces_mask(chess.PAWN, chess.BLACK).bit_count() * -1)
        estimatedUtility += (chessBoard.pieces_mask(chess.BISHOP, chess.BLACK).bit_count() * -3)
        estimatedUtility += (chessBoard.pieces_mask(chess.KNIGHT, chess.BLACK).bit_count() * -3)
        estimatedUtility += (chessBoard.pieces_mask(chess.ROOK, chess.BLACK).bit_count() * -5)
        estimatedUtility += (chessBoard.pieces_mask(chess.QUEEN, chess.BLACK).bit_count() * -9)

        return estimatedUtility




