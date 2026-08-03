from unittest import result
import math
import random
import chess
from chess_adversarial_search.misc import Timer

class Game:

    def __init__(self):
        self.__pieceBasicUtilityDictionary = {
            'P': 1,
            'R': 5,
            'B': 3,
            'N': 3,
            'Q': 9,
            'p': -1,
            'r': -5,
            'b': -3,
            'n': -3,
            'q': -9
        }

    def toMove(self, chessBoard):
        return chessBoard.turn

    def actions(self, chessBoard):
        # May need to adapt this for the promotion if material is not available
        return list(chessBoard.legal_moves)

    def result(self, chessBoard, move):
        chessBoard.push(move)
        return chessBoard

    def reverseMove(self, chessBoard):
        return chessBoard.pop()

    def isTerminal(self, chessBoard):
        ## This may need expanding ##
        return chessBoard.is_game_over()

    def utility(self, chessBoard):
        # Check if the game is over
        resultStr = chessBoard.result()
        if resultStr != '*':
            # For the time being a draw is assigned a zero (this may need changing)
            if resultStr == '1/2-1/2':
                return 0
            # We now know that the score is either '1-0' or '0-1'
            if resultStr == '1-0':
                # White wins
                return 99999
            elif resultStr == '0-1':
                # Black wins
                return -99999

        return self.__Evaluation(chessBoard)

    def __Evaluation(self, chessBoard):
        utility = 0

        utility += (chessBoard.pieces_mask(chess.PAWN, chess.WHITE).bit_count() * 1)
        utility += (chessBoard.pieces_mask(chess.BISHOP, chess.WHITE).bit_count() * 3)
        utility += (chessBoard.pieces_mask(chess.KNIGHT, chess.WHITE).bit_count() * 3)
        utility += (chessBoard.pieces_mask(chess.ROOK, chess.WHITE).bit_count() * 5)
        utility += (chessBoard.pieces_mask(chess.QUEEN, chess.WHITE).bit_count() * 9)

        utility += (chessBoard.pieces_mask(chess.PAWN, chess.BLACK).bit_count() * -1)
        utility += (chessBoard.pieces_mask(chess.BISHOP, chess.BLACK).bit_count() * -3)
        utility += (chessBoard.pieces_mask(chess.KNIGHT, chess.BLACK).bit_count() * -3)
        utility += (chessBoard.pieces_mask(chess.ROOK, chess.BLACK).bit_count() * -5)
        utility += (chessBoard.pieces_mask(chess.QUEEN, chess.BLACK).bit_count() * -9)

        return utility




