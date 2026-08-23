import copy

from piece_path_finding.board_state import BoardState
from piece_path_finding.piece_path_finding_config import initialBoardStartStateDictionary
from piece_path_finding.action import Action
from piece_path_finding.best_first_search import bestFirstSearch
from piece_path_finding.problem import Problem
from piece_path_finding.solution_handler import SolutionHandler

class BasicBoardManager:
    def __init__(self, communicationManager):
        self._communicationManager = communicationManager

        self._boardState = self._loadBoardState()

        if self._boardState is None:
            self._boardState = BoardState(boardStateDictionary=initialBoardStartStateDictionary)


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
        initialPosition = str(move.uci()[0:2])
        destinationPosition = str(move.uci()[2:4])

        if ((move.promotion is not None) and chessBoard.is_capture(move)):

            pass
            #Victim to graveyard
            #Pawn to graveyard
            #Promoted from graveyard to destination
        elif chessBoard.is_capture(move):
            pass
            #Victim to graveyard
            #Attacker to destination
        elif move.promotion is not None:
            pass
            #Pawn to graveyard
            #Promoted from graveyard to destination
        elif chessBoard.is_kingside_castling(move):
            pass
            # King to destination
            # Rook to destination
        elif chessBoard.is_queenside_castling(move):
            pass
            # King to destination
            # Rook to destination
        else:
            initialPosition = self._chessSquareToBoardGridXY(initialPosition)
            destination = self._chessSquareToBoardGridXY(destinationPosition)
            piece = self._boardState.getPieceAtLocation(initialPosition)
            action = Action(piece=piece, initialPosition=initialPosition, destination=destination)
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




