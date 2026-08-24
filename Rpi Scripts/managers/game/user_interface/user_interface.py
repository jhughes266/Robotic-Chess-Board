from abc import ABC, abstractmethod
import os
class UserInterface(ABC):
    def __init__(self):
        self._chessColourAsText = ['Black', 'White']

    @abstractmethod
    def playerSelectMove(self, chessBoard):
        pass

    @abstractmethod
    def claimDraw(self, chessBoard):
        pass

    @abstractmethod
    def moveInfo(self, chessBoard):
        pass

    @abstractmethod
    def resultingMoveInfo(self, chessBoard, move):
        pass

    @abstractmethod
    def gameResultInfo(self, chessBoard):
        pass

class TextUserInterface(UserInterface):
    def playerSelectMove(self, chessBoard):
        selectedMove = None
        legalMoveMade = False
        while not legalMoveMade:
            candidateMove = input("Please enter your move!: ")
            legalMoves = list(chessBoard.legal_moves)
            for move in legalMoves:
                if str(move) == candidateMove:
                    legalMoveMade = True
                    selectedMove = candidateMove
                    break

            if not legalMoveMade:
                print("The move that you have selected is illegal! Please re-enter your move!")

        return selectedMove

    def claimDraw(self, chessBoard):

        while chessBoard.can_claim_draw():
            if chessBoard.can_claim_fifty_moves():
                selection = input("It has been 50 consecutive moves without a capture or pawn move would you like to claim a draw?:\nEnter NO or YES:\nSelection: ")
            else:
                selection = input("The exact same three positions have occurred during the game! Would you like to claim a draw?:\nEnter NO or YES:\nSelection: ")

            if selection == "NO":
                return False
            elif selection == "YES":
                return True
            else:
                print("The selection was not recognized. Please re-enter your selection!")

        return False

    def moveInfo(self, chessBoard):
        print(f"%%%%%%%%%%%%%%%%%%%%%%%\nIt is {self._chessColourAsText[chessBoard.turn]} turn to move.The state of the board is:\n{chessBoard}")

    def resultingMoveInfo(self, chessBoard, move):
        print(f"The move made was {move}.\nThe state of the board after this move is:\n{str(chessBoard)}\n%%%%%%%%%%%%%%%%%%%%%%%")

    def gameResultInfo(self, chessBoard):
        resultStr = chessBoard.result()
        if resultStr == '1-0':
            # White wins
            print("White Wins!\n\n\n")
        elif resultStr == '0-1':
            # Black wins
            print("Black Wins!\n\n\n")
        else:
            print("The game is drawn!\n\n\n")