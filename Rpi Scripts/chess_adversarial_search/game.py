from unittest import result
import math
import random
import chess

class Game:

    def __init__(self, maxPlyDepth):
        self.__maxPlyDepth = maxPlyDepth
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
        self.__previousUtility = 0

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

    def isTerminal(self, chessBoard, plyDepth):
        ## This may need expanding ##
        return plyDepth == self.__maxPlyDepth or chessBoard.is_game_over()

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

        return self.__BasicUtility(chessBoard)


    def __BasicUtility(self, chessBoard):
        fen = chessBoard.fen()
        fenIdx = 0
        utility = 0
        while fen[fenIdx] != ' ':
            currentPiece = fen[fenIdx]
            if currentPiece in self.__pieceBasicUtilityDictionary:
                utility += self.__pieceBasicUtilityDictionary[currentPiece]
            fenIdx += 1

        return utility



