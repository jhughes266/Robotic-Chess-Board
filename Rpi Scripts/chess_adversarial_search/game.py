from unittest import result
import math
import random
import chess
from chess_adversarial_search.misc import Timer
import copy

class Game:
    # Class vars
    EARLY_MIDDLE_GAME = 0
    END_GAME = 1

    def __init__(self, boardManager):
        self.__boardManager = boardManager
        self.__pieceSquareTables = PieceSquareTables()

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

    def utility(self, chessBoard, plyDepth):
        resultStr = chessBoard.result()
        # For the time being a draw is assigned a zero (this may need changing)
        if resultStr == '1/2-1/2':
            return 0
        # We now know that the score is either '1-0' or '0-1'
        elif resultStr == '1-0':
            # White wins
            return 999999 - plyDepth
        elif resultStr == '0-1':
            # Black wins
            return -999999 + plyDepth
        else:
            raise RuntimeError("Attempted to calculate utility but the game was not in a terminal state!")

    def evaluate(self, chessBoard):
        materialValue = 0

        materialValue += (chessBoard.pieces_mask(chess.PAWN, chess.WHITE).bit_count() * 100)
        materialValue += (chessBoard.pieces_mask(chess.BISHOP, chess.WHITE).bit_count() * 300)
        materialValue += (chessBoard.pieces_mask(chess.KNIGHT, chess.WHITE).bit_count() * 300)
        materialValue += (chessBoard.pieces_mask(chess.ROOK, chess.WHITE).bit_count() * 500)
        materialValue += (chessBoard.pieces_mask(chess.QUEEN, chess.WHITE).bit_count() * 900)

        materialValue += (chessBoard.pieces_mask(chess.PAWN, chess.BLACK).bit_count() * -100)
        materialValue += (chessBoard.pieces_mask(chess.BISHOP, chess.BLACK).bit_count() * -300)
        materialValue += (chessBoard.pieces_mask(chess.KNIGHT, chess.BLACK).bit_count() * -300)
        materialValue += (chessBoard.pieces_mask(chess.ROOK, chess.BLACK).bit_count() * -500)
        materialValue += (chessBoard.pieces_mask(chess.QUEEN, chess.BLACK).bit_count() * -900)

        gamePhase = self.__evaluateGamePhase(chessBoard)
        positionEvaluation = self.__pieceSquareTables.evaluate(chessBoard, gamePhase)
        estimatedUtility = materialValue + positionEvaluation

        return estimatedUtility

    def __evaluateGamePhase(self, chessBoard):
        whiteQueens = chessBoard.pieces_mask(chess.QUEEN, chess.WHITE).bit_count()
        whiteRooks = chessBoard.pieces_mask(chess.ROOK, chess.WHITE).bit_count()
        whiteBishops = chessBoard.pieces_mask(chess.BISHOP, chess.WHITE).bit_count()
        whiteKnights = chessBoard.pieces_mask(chess.KNIGHT, chess.WHITE).bit_count()

        blackQueens = chessBoard.pieces_mask(chess.QUEEN, chess.BLACK).bit_count()
        blackRooks = chessBoard.pieces_mask(chess.ROOK, chess.BLACK).bit_count()
        blackBishops = chessBoard.pieces_mask(chess.BISHOP, chess.BLACK).bit_count()
        blackKnights = chessBoard.pieces_mask(chess.KNIGHT, chess.BLACK).bit_count()

        whiteIsInEndGame = ((whiteQueens == 1) and (whiteRooks == 0) and (whiteBishops + whiteKnights <= 1)) or (whiteQueens == 0)

        blackIsInEndGame = ((blackQueens == 1) and (blackRooks == 0) and (blackBishops + blackKnights <= 1)) or (blackQueens == 0)

        if whiteIsInEndGame and blackIsInEndGame:
            return Game.END_GAME

        return Game.EARLY_MIDDLE_GAME

class PieceSquareTables:
    def __init__(self):
        # The reversal is necessary because the python chess library labels the bottom left square as incrementing left
        # to right up the board. List Indexing goes the top left right to left down the board. The board is symmetrical
        # "down the middle" so no other operations need to be performed.
        #White pieces
        self.__pawnWhite = [ 0,  0,  0,  0,  0,  0,  0,  0,
                            50, 50, 50, 50, 50, 50, 50, 50,
                            10, 10, 20, 30, 30, 20, 10, 10,
                             5,  5, 10, 25, 25, 10,  5,  5,
                             0,  0,  0, 20, 20,  0,  0,  0,
                             5, -5,-10,  0,  0,-10, -5,  5,
                             5, 10, 10,-20,-20, 10, 10,  5,
                             0,  0,  0,  0,  0,  0,  0,  0]
        self.__pawnWhite.reverse()
        self.__knightWhite = [-50,-40,-30,-30,-30,-30,-40,-50,
                              -40,-20,  0,  0,  0,  0,-20,-40,
                              -30,  0, 10, 15, 15, 10,  0,-30,
                              -30,  5, 15, 20, 20, 15,  5,-30,
                              -30,  0, 15, 20, 20, 15,  0,-30,
                              -30,  5, 10, 15, 15, 10,  5,-30,
                              -40,-20,  0,  5,  5,  0,-20,-40,
                              -50,-40,-30,-30,-30,-30,-40,-50]
        self.__knightWhite.reverse()
        self.__bishopWhite = [-20,-10,-10,-10,-10,-10,-10,-20,
                              -10,  0,  0,  0,  0,  0,  0,-10,
                              -10,  0,  5, 10, 10,  5,  0,-10,
                              -10,  5,  5, 10, 10,  5,  5,-10,
                              -10,  0, 10, 10, 10, 10,  0,-10,
                              -10, 10, 10, 10, 10, 10, 10,-10,
                              -10,  5,  0,  0,  0,  0,  5,-10,
                              -20,-10,-10,-10,-10,-10,-10,-20]
        self.__bishopWhite.reverse()
        self.__rookWhite = [0,  0,  0,  0,  0,  0,  0,  0,
                            5, 10, 10, 10, 10, 10, 10,  5,
                           -5,  0,  0,  0,  0,  0,  0, -5,
                           -5,  0,  0,  0,  0,  0,  0, -5,
                           -5,  0,  0,  0,  0,  0,  0, -5,
                           -5,  0,  0,  0,  0,  0,  0, -5,
                           -5,  0,  0,  0,  0,  0,  0, -5,
                            0,  0,  0,  5,  5,  0,  0,  0]
        self.__rookWhite.reverse()
        self.__queenWhite = [-20,-10,-10, -5, -5,-10,-10,-20,
                             -10,  0,  0,  0,  0,  0,  0,-10,
                             -10,  0,  5,  5,  5,  5,  0,-10,
                              -5,  0,  5,  5,  5,  5,  0, -5,
                               0,  0,  5,  5,  5,  5,  0, -5,
                             -10,  5,  5,  5,  5,  5,  0,-10,
                             -10,  0,  5,  0,  0,  0,  0,-10,
                             -20,-10,-10, -5, -5,-10,-10,-20]
        self.__queenWhite.reverse()
        self.__kingEarlyMiddleWhite = [-30,-40,-40,-50,-50,-40,-40,-30,
                                       -30,-40,-40,-50,-50,-40,-40,-30,
                                       -30,-40,-40,-50,-50,-40,-40,-30,
                                       -30,-40,-40,-50,-50,-40,-40,-30,
                                       -20,-30,-30,-40,-40,-30,-30,-20,
                                       -10,-20,-20,-20,-20,-20,-20,-10,
                                        20, 20,  0,  0,  0,  0, 20, 20,
                                        20, 30, 10,  0,  0, 10, 30, 20]
        self.__kingEarlyMiddleWhite.reverse()
        self.__kingEndWhite = [-50,-40,-30,-20,-20,-30,-40,-50,
                               -30,-20,-10,  0,  0,-10,-20,-30,
                               -30,-10, 20, 30, 30, 20,-10,-30,
                               -30,-10, 30, 40, 40, 30,-10,-30,
                               -30,-10, 30, 40, 40, 30,-10,-30,
                               -30,-10, 20, 30, 30, 20,-10,-30,
                               -30,-30,  0,  0,  0,  0,-30,-30,
                               -50,-30,-30,-30,-30,-30,-30,-50]
        self.__kingEndWhite.reverse()

        self.__pawnBlack = self.__pawnWhite[::-1]
        self.__pawnBlack = [positionValue * -1 for positionValue in self.__pawnBlack]
        self.__knightBlack = self.__knightWhite[::-1]
        self.__knightBlack = [positionValue * -1 for positionValue in self.__knightBlack]
        self.__bishopBlack = self.__bishopWhite[::-1]
        self.__bishopBlack = [positionValue * -1 for positionValue in self.__bishopBlack]
        self.__rookBlack = self.__rookWhite[::-1]
        self.__rookBlack = [positionValue * -1 for positionValue in self.__rookBlack]
        self.__queenBlack = self.__queenWhite[::-1]
        self.__queenBlack = [positionValue * -1 for positionValue in self.__queenBlack]
        self.__kingEarlyMiddleBlack = self.__kingEarlyMiddleWhite[::-1]
        self.__kingEarlyMiddleBlack = [positionValue * -1 for positionValue in self.__kingEarlyMiddleBlack]
        self.__kingEndBlack = self.__kingEndWhite[::-1]
        self.__kingEndBlack = [positionValue * -1 for positionValue in self.__kingEndBlack]

        # Storing in dictionary for easy access later
        self.__pieceTableDict = {
            'pawnWhite' : self.__pawnWhite,
            'knightWhite' : self.__knightWhite,
            'bishopWhite' : self.__bishopWhite,
            'rookWhite' : self.__rookWhite,
            'queenWhite' : self.__queenWhite,
            'kingEarlyMiddleWhite' : self.__kingEarlyMiddleWhite,
            'kingEndWhite' : self.__kingEndWhite,

            'pawnBlack' : self.__pawnBlack,
            'knightBlack' : self.__knightBlack,
            'bishopBlack' : self.__bishopBlack,
            'rookBlack' : self.__rookBlack,
            'queenBlack' : self.__queenBlack,
            'kingEarlyMiddleBlack' : self.__kingEarlyMiddleBlack,
            'kingEndBlack' : self.__kingEndBlack
        }

        # Dictionary for mapping from previous dictionary names to a python chess piece
        self.__nameToChessPiece = {
            'pawnWhite' : chess.PAWN,
            'knightWhite' : chess.KNIGHT,
            'bishopWhite' : chess.BISHOP,
            'rookWhite' : chess.ROOK,
            'queenWhite' : chess.QUEEN,
            'kingEarlyMiddleWhite': chess.KING,
            'kingEndWhite' : chess.KING,

            'pawnBlack': chess.PAWN,
            'knightBlack': chess.KNIGHT,
            'bishopBlack': chess.BISHOP,
            'rookBlack': chess.ROOK,
            'queenBlack': chess.QUEEN,
            'kingEarlyMiddleBlack': chess.KING,
            'kingEndBlack': chess.KING,
        }

        #Dictionary for mapping from name to colour
        self.__nameToColour = {
            'pawnWhite' : chess.WHITE,
            'knightWhite' : chess.WHITE,
            'bishopWhite' : chess.WHITE,
            'rookWhite' : chess.WHITE,
            'queenWhite' : chess.WHITE,
            'kingEarlyMiddleWhite': chess.WHITE,
            'kingEndWhite' : chess.WHITE,

            'pawnBlack': chess.BLACK,
            'knightBlack': chess.BLACK,
            'bishopBlack': chess.BLACK,
            'rookBlack': chess.BLACK,
            'queenBlack': chess.BLACK,
            'kingEarlyMiddleBlack': chess.BLACK,
            'kingEndBlack': chess.BLACK,
        }

    def evaluate(self, chessBoard, gamePhase):

        positionEvaluation = 0
        for pieceTableKey in self.__pieceTableDict:
            pieceTable = self.__pieceTableDict[pieceTableKey]
            pythonChessPiece = self.__nameToChessPiece[pieceTableKey]
            pythonChessColour = self.__nameToColour[pieceTableKey]

            for square in chessBoard.pieces(pythonChessPiece, pythonChessColour):
                positionEvaluation += pieceTable[square]

        return positionEvaluation


    def printTable(self, table):

        for i, val in enumerate(table[::-1]):
            if val < 10 and val >= 0:
                print("  ", end="")
            elif val >= 10:
                print(" ", end="")
            elif val < 0 and val > -10:
                print(" ", end="")

            print(val, end=",")
            if (i+1) % 8 == 0:
                print()






