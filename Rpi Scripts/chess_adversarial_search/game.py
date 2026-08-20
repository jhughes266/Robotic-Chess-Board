from unittest import result
import math
import random
import chess
from chess_adversarial_search.misc import Timer

class Game:
    # Class vars
    EARLY_MIDDLE_GAME = 0
    END_GAME = 1

    def __init__(self):
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
        pawn = [ 0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                 5,  5, 10, 25, 25, 10,  5,  5,
                 0,  0,  0, 20, 20,  0,  0,  0,
                 5, -5,-10,  0,  0,-10, -5,  5,
                 5, 10, 10,-20,-20, 10, 10,  5,
                 0,  0,  0,  0,  0,  0,  0,  0]
        knight = [-50,-40,-30,-30,-30,-30,-40,-50,
                  -40,-20,  0,  0,  0,  0,-20,-40,
                  -30,  0, 10, 15, 15, 10,  0,-30,
                  -30,  5, 15, 20, 20, 15,  5,-30,
                  -30,  0, 15, 20, 20, 15,  0,-30,
                  -30,  5, 10, 15, 15, 10,  5,-30,
                  -40,-20,  0,  5,  5,  0,-20,-40,
                  -50,-40,-30,-30,-30,-30,-40,-50]
        bishop = [-20,-10,-10,-10,-10,-10,-10,-20,
                  -10,  0,  0,  0,  0,  0,  0,-10,
                  -10,  0,  5, 10, 10,  5,  0,-10,
                  -10,  5,  5, 10, 10,  5,  5,-10,
                  -10,  0, 10, 10, 10, 10,  0,-10,
                  -10, 10, 10, 10, 10, 10, 10,-10,
                  -10,  5,  0,  0,  0,  0,  5,-10,
                  -20,-10,-10,-10,-10,-10,-10,-20]
        rook = [0,  0,  0,  0,  0,  0,  0,  0,
                5, 10, 10, 10, 10, 10, 10,  5,
               -5,  0,  0,  0,  0,  0,  0, -5,
               -5,  0,  0,  0,  0,  0,  0, -5,
               -5,  0,  0,  0,  0,  0,  0, -5,
               -5,  0,  0,  0,  0,  0,  0, -5,
               -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0]
        queen = [-20,-10,-10, -5, -5,-10,-10,-20,
                 -10,  0,  0,  0,  0,  0,  0,-10,
                 -10,  0,  5,  5,  5,  5,  0,-10,
                  -5,  0,  5,  5,  5,  5,  0, -5,
                   0,  0,  5,  5,  5,  5,  0, -5,
                 -10,  5,  5,  5,  5,  5,  0,-10,
                 -10,  0,  5,  0,  0,  0,  0,-10,
                 -20,-10,-10, -5, -5,-10,-10,-20]
        kingEarlyMiddle = [-30,-40,-40,-50,-50,-40,-40,-30,
                           -30,-40,-40,-50,-50,-40,-40,-30,
                           -30,-40,-40,-50,-50,-40,-40,-30,
                           -30,-40,-40,-50,-50,-40,-40,-30,
                           -20,-30,-30,-40,-40,-30,-30,-20,
                           -10,-20,-20,-20,-20,-20,-20,-10,
                            20, 20,  0,  0,  0,  0, 20, 20,
                            20, 30, 10,  0,  0, 10, 30, 20]
        kingEnd = [-50,-40,-30,-20,-20,-30,-40,-50,
                   -30,-20,-10,  0,  0,-10,-20,-30,
                   -30,-10, 20, 30, 30, 20,-10,-30,
                   -30,-10, 30, 40, 40, 30,-10,-30,
                   -30,-10, 30, 40, 40, 30,-10,-30,
                   -30,-10, 20, 30, 30, 20,-10,-30,
                   -30,-30,  0,  0,  0,  0,-30,-30,
                   -50,-30,-30,-30,-30,-30,-30,-50]

        pawnSquareTableBitMapDictionary = self.__constructPieceSquareTableBitMap(pawn)
        knightSquareTableBitMapDictionary = self.__constructPieceSquareTableBitMap(knight)
        bishopSquareTableBitMapDictionary = self.__constructPieceSquareTableBitMap(bishop)
        rookSquareTableBitMapDictionary = self.__constructPieceSquareTableBitMap(rook)
        queenSquareTableBitMapDictionary = self.__constructPieceSquareTableBitMap(queen)
        kingSquareTableEarlyMiddleBitMapDictionary = self.__constructPieceSquareTableBitMap(kingEarlyMiddle)
        kingEndSquareTableBitMapDictionary = self.__constructPieceSquareTableBitMap(kingEnd)

        self.__allSquareTableBitMapDictionaries = {
            'pawn' : pawnSquareTableBitMapDictionary,
            'knight' : knightSquareTableBitMapDictionary,
            'bishop': bishopSquareTableBitMapDictionary,
            'rook' : rookSquareTableBitMapDictionary,
            'queen' : queenSquareTableBitMapDictionary,
            'kingEarlyMiddle' : kingSquareTableEarlyMiddleBitMapDictionary,
            'kingEnd' : kingEndSquareTableBitMapDictionary
        }

        self.__pieceSquareTableNameToChessPieceId = {
            'pawn' : chess.PAWN,
            'knight' : chess.KNIGHT,
            'bishop': chess.BISHOP,
            'rook' : chess.ROOK,
            'queen' : chess.QUEEN,
            'kingEarlyMiddle' : chess.KING,
            'kingEnd' : chess.KING
        }

    def evaluate(self, chessBoard, gamePhase):

        for piece in self.__allSquareTableBitMapDictionaries:
            currentSquareTablePieceBitMapDictionary = self.__allSquareTableBitMapDictionaries[piece]
            currentWhitePiecePositionBitMap = chessBoard.pieces_mask(self.__pieceSquareTableNameToChessPieceId[piece], chess.WHITE)
            currentBlackPiecePositionBitMap = chessBoard.pieces_mask(self.__pieceSquareTableNameToChessPieceId[piece], chess.BLACK)
            for uniquePosEval in currentSquareTablePieceBitMapDictionary:
                 currentUniquePosEvalBitMap = bin(currentSquareTablePieceBitMapDictionary[uniquePosEval])




    def __constructPieceSquareTableBitMap(self, pieceSquareTable):
        unqiueNumberSet = set(pieceSquareTable)
        bitMapDictionary = {}
        for unqiueNumber in unqiueNumberSet:
            bitMap = ""
            for positionalValue in pieceSquareTable:
                bitMap += str(int(positionalValue == unqiueNumber))
            bitMapDictionary[unqiueNumber] = int(bitMap, 2)

        return bitMapDictionary

    def printBitMap(self, bitMap):
        bitMapString = str(bitMap)[2:]
        additionalZerosNeeded = 64 - len(bitMapString)
        additionalZeros = "0" * additionalZerosNeeded
        bitMapString = additionalZeros + bitMapString
        for i, bit in enumerate(bitMapString):
            print(bit, end=",")
            if (i + 1) % 8 == 0:
                print()








