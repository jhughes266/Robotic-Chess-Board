from piece_path_finding.board_state import BoardState
from piece_path_finding.piece_path_finding_config import initialBoardStartStateDictionary
from piece_path_finding.action import Action
from piece_path_finding.best_first_search import bestFirstSearch
from piece_path_finding.problem import Problem
from piece_path_finding.solution_handler import SolutionHandler
import chess

class BoardManager:
    def __init__(self, communicationManager):
        self._communicationManager = communicationManager

        self._boardState = self._loadBoardState()

        if self._boardState is None:
            self._boardState = BoardState(boardStateDictionary=initialBoardStartStateDictionary)

        print(self._boardState)

    def _chessSquareToBoardGridXY(self, square):
        file = square[0]
        rank = square[1]
        gridX = ord(file) - 95
        gridY = int(rank) + 1
        return [gridX, gridY]

    def _loadBoardState(self):
        return None

    def executeMove(self, move, chessBoard):
        goalBoardState = None
        initialPosition = self._chessSquareToBoardGridXY(move.uci()[0:2])
        destinationPosition = self._chessSquareToBoardGridXY(move.uci()[2:4])

        if ((move.promotion is not None) and chessBoard.is_capture(move)):
            # Pawn
            pawnInitialPosition = initialPosition
            # The pawn is from the player who is moving
            pawnColour = chessBoard.turn
            pawnDestinationPosition = self._boardState.findFreeGraveSpace(pawnColour)
            pawnPiece = self._boardState.getPieceAtLocation(pawnInitialPosition)
            pawnKillAction = Action(piece=pawnPiece, initialPosition=pawnInitialPosition,
                                    destination=pawnDestinationPosition)
            goalBoardState = self._boardState.resultantStateAfterAction(pawnKillAction)

            # Victim
            victimInitialPosition = destinationPosition
            # The move hasn't been executed yet so it is the attackers turn. So the opposite colour is the victim
            victimColour = not (chessBoard.turn)
            victimDestinationPosition = goalBoardState.findFreeGraveSpace(victimColour)
            victimPiece = goalBoardState.getPieceAtLocation(victimInitialPosition)
            victimAction = Action(piece=victimPiece, initialPosition=victimInitialPosition,
                                  destination=victimDestinationPosition)
            goalBoardState = goalBoardState.resultantStateAfterAction(victimAction)

            # Promoted Piece
            promotedPiecePrefix = move.uci()[5]
            colourOfPromotedPiece = chessBoard.turn
            if colourOfPromotedPiece == chess.WHITE:
                promotedPiecePrefix = promotedPiecePrefix.upper()
            promotedInitialPosition = goalBoardState.findDeadPieceLocation(promotedPiecePrefix)
            promotedPiece = goalBoardState.getPieceAtLocation(promotedInitialPosition)
            promotedDestinationPosition = destinationPosition
            promotionAction = Action(piece=promotedPiece, initialPosition=promotedInitialPosition,
                                     destination=promotedDestinationPosition)
            goalBoardState = goalBoardState.resultantStateAfterAction(promotionAction)

        elif chessBoard.is_capture(move):
            # Victim
            victimInitialPosition = destinationPosition
            # The move hasn't been executed yet so it is the attackers turn. So the opposite colour is the victim
            victimColour = not (chessBoard.turn)
            victimDestinationPosition = self._boardState.findFreeGraveSpace(victimColour)
            victimPiece = self._boardState.getPieceAtLocation(victimInitialPosition)
            victimAction = Action(piece=victimPiece, initialPosition=victimInitialPosition,
                                  destination=victimDestinationPosition)
            goalBoardState = self._boardState.resultantStateAfterAction(victimAction)

            # Attack
            attackerInitialPosition = initialPosition
            attackerDestinationPosition = destinationPosition
            attackingPiece = goalBoardState.getPieceAtLocation(attackerInitialPosition)
            attackerAction = Action(piece=attackingPiece, initialPosition=attackerInitialPosition, destination=attackerDestinationPosition)
            goalBoardState = goalBoardState.resultantStateAfterAction(attackerAction)

        elif move.promotion is not None:
            # Pawn
            pawnInitialPosition = initialPosition
            # The pawn is from the player who is moving
            pawnColour = chessBoard.turn
            pawnDestinationPosition = self._boardState.findFreeGraveSpace(pawnColour)
            pawnPiece = self._boardState.getPieceAtLocation(pawnInitialPosition)
            pawnKillAction = Action(piece=pawnPiece, initialPosition=pawnInitialPosition,
                                    destination=pawnDestinationPosition)
            goalBoardState = self._boardState.resultantStateAfterAction(pawnKillAction)

            # Promotion
            promotedPiecePrefix = move.uci()[5]
            colourOfPromotedPiece = chessBoard.turn
            if colourOfPromotedPiece == chess.WHITE:
                promotedPiecePrefix = promotedPiecePrefix.upper()
            promotedInitialPosition = goalBoardState.findDeadPieceLocation(promotedPiecePrefix)
            promotedPiece = goalBoardState.getPieceAtLocation(promotedInitialPosition)
            promotedDestinationPosition = destinationPosition
            promotionAction = Action(piece=promotedPiece, initialPosition=promotedInitialPosition,
                                     destination=promotedDestinationPosition)
            goalBoardState = goalBoardState.resultantStateAfterAction(promotionAction)

        elif chessBoard.is_kingside_castling(move):
            # King to destination
            kingInitialPosition = initialPosition
            kingDestinationPosition = destinationPosition
            piece = self._boardState.getPieceAtLocation(kingInitialPosition)
            action = Action(piece=piece, initialPosition=kingInitialPosition, destination=kingDestinationPosition)
            goalBoardState = self._boardState.resultantStateAfterAction(action)

            # Rook to destination
            rookInitialPosition = kingInitialPosition[:]
            rookInitialPosition[0] += 3
            rookDestinationPosition = kingInitialPosition[:]
            rookDestinationPosition[0] += 1
            piece = goalBoardState.getPieceAtLocation(initialPosition)
            action = Action(piece=piece, initialPosition=rookInitialPosition, destination=rookDestinationPosition)
            goalBoardState = goalBoardState.resultantStateAfterAction(action)

        elif chessBoard.is_queenside_castling(move):
            # King to destination
            kingInitialPosition = initialPosition
            kingDestinationPosition = destinationPosition
            piece = self._boardState.getPieceAtLocation(kingInitialPosition)
            action = Action(piece=piece, initialPosition=kingInitialPosition, destination=kingDestinationPosition)
            goalBoardState = self._boardState.resultantStateAfterAction(action)

            # Rook to destination
            rookInitialPosition = kingInitialPosition[:]
            rookInitialPosition[0] -= 4
            rookDestinationPosition = kingInitialPosition[:]
            rookDestinationPosition[0] -= 1
            piece = goalBoardState.getPieceAtLocation(initialPosition)
            action = Action(piece=piece, initialPosition=rookInitialPosition, destination=rookDestinationPosition)
            goalBoardState = goalBoardState.resultantStateAfterAction(action)

        elif chessBoard.is_en_passant(move):
            # Victim Pawn
            # There needs to be an offset because the pawn is either up or down depending on the capturing side.
            vivictimYOffset = -1
            if chessBoard.turn == chess.BLACK:
                victimYOffset = +1
            victimInitialPosition = destinationPosition[:]
            victimInitialPosition[1] += victimYOffset
            # The move hasn't been executed yet so it is the attackers turn. So the opposite colour is the victim
            victimColour = not (chessBoard.turn)
            victimDestinationPosition = self._boardState.findFreeGraveSpace(victimColour)
            victimPiece = self._boardState.getPieceAtLocation(victimInitialPosition)
            victimAction = Action(piece=victimPiece, initialPosition=victimInitialPosition,
                                  destination=victimDestinationPosition)
            goalBoardState = self._boardState.resultantStateAfterAction(victimAction)

            # Attack
            attackerInitialPosition = initialPosition
            attackerDestinationPosition = destinationPosition
            attackingPiece = goalBoardState.getPieceAtLocation(attackerInitialPosition)
            attackerAction = Action(piece=attackingPiece, initialPosition=attackerInitialPosition,
                                    destination=attackerDestinationPosition)
            goalBoardState = goalBoardState.resultantStateAfterAction(attackerAction)
        else:
            # Piece
            pieceInitialPosition = initialPosition
            pieceDestinationPosition = destinationPosition
            piece = self._boardState.getPieceAtLocation(pieceInitialPosition)
            action = Action(piece=piece, initialPosition=pieceInitialPosition, destination=pieceDestinationPosition)
            goalBoardState = self._boardState.resultantStateAfterAction(action)


        problem = Problem(initialState=self._boardState, goalState=goalBoardState)
        solutionNode = bestFirstSearch(problem)
        testSolutionHandler = SolutionHandler(solutionNode)
        print(testSolutionHandler)
        self._boardState = goalBoardState


    def gameEndMessage(self):
        pass

    def resetBoard(self):
        pass




