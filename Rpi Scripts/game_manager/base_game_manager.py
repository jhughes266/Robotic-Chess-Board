import chess
from chess_adversarial_search.game import Game
from chess_adversarial_search.minimax_alpha_beta import timeBoundedMinimaxAlphaBetaSearch



class GameManager:
    def __init__(self):
        self._gameMode = None
        self._maxSearchTimeSeconds = 5

    def selectMode(self):
        acceptableModes = {'1', '2', '3', '4'}
        while True:
            self._gameMode = input(
                "Select game mode!\nEnter 1 for white human player vs black robot\nEnter 2 for black human player vs black white\nEnter 3 for human vs human\nEnter 4 for Robot vs Robot \nSelection : ")

            if self._gameMode in acceptableModes:
                break

            print("You have not selected the right game mode!\n")

    def playGame(self):
        chessBoard = chess.Board()
        game = Game()
        print(f"The initial board state is:\n{str(chessBoard)}")
        while True:

            if self._gameMode == '1':
                playerMove = chess.Move.from_uci(self._selectMove("white", chessBoard))
                chessBoard.push(playerMove)
                print(f"The white players move was {playerMove}.\nThe state of the board after this move is:\n{str(chessBoard)}")
                if chessBoard.is_game_over():
                    break

                self._engineMoveInfo("black")
                engineMove = timeBoundedMinimaxAlphaBetaSearch(game, chessBoard, maxSearchTimeSeconds=self._maxSearchTimeSeconds)
                chessBoard.push(engineMove)
                print(f"The black robot move was {engineMove}.\nThe state of the board after this move is:\n{str(chessBoard)}")
                if chessBoard.is_game_over():
                    break


            elif self._gameMode == '2':
                self._engineMoveInfo("white")
                engineMove = timeBoundedMinimaxAlphaBetaSearch(game, chessBoard, maxSearchTimeSeconds=self._maxSearchTimeSeconds)
                chessBoard.push(engineMove)
                print(f"The white robot move was {engineMove}.\nThe state of the board after this move is:\n{str(chessBoard)}")
                if chessBoard.is_game_over():
                    break

                playerMove = chess.Move.from_uci(self._selectMove("black", chessBoard))
                chessBoard.push(playerMove)
                print(f"The black players move was {playerMove}.\nThe state of the board after this move is:\n{str(chessBoard)}")
                if chessBoard.is_game_over():
                    break

            elif self._gameMode == '3':
                playerMove = chess.Move.from_uci(self._selectMove("white", chessBoard))
                chessBoard.push(playerMove)
                print(f"The white players move was {playerMove}.\nThe state of the board after this move is:\n{str(chessBoard)}")
                if chessBoard.is_game_over():
                    break

                playerMove = chess.Move.from_uci(self._selectMove("black", chessBoard))
                chessBoard.push(playerMove)
                print(f"The black players move was {playerMove}.\nThe state of the board after this move is:\n{str(chessBoard)}")
                if chessBoard.is_game_over():
                    break

            elif self._gameMode == '4':
                self._engineMoveInfo("white")
                engineMove = timeBoundedMinimaxAlphaBetaSearch(game, chessBoard,maxSearchTimeSeconds=self._maxSearchTimeSeconds)
                chessBoard.push(engineMove)
                print(f"The white robot move was {engineMove}.\nThe state of the board after this move is:\n{str(chessBoard)}")
                if chessBoard.is_game_over():
                    break

                self._engineMoveInfo("black")
                engineMove = timeBoundedMinimaxAlphaBetaSearch(game, chessBoard,maxSearchTimeSeconds=self._maxSearchTimeSeconds)
                chessBoard.push(engineMove)
                print(f"The white robot move was {engineMove}.\nThe state of the board after this move is:\n{str(chessBoard)}")
                if chessBoard.is_game_over():
                    break

        resultStr = chessBoard.result()
        if resultStr == '1/2-1/2':
            print("Draw")
        elif resultStr == '1-0':
            # White wins
            print("White Wins")
        elif resultStr == '0-1':
            # Black wins
            print("Black Wins")

    def _selectMove(self, colour, chessBoard):
        selectedMove = None
        legalMoveMade = False
        while not legalMoveMade:
            candidateMove = input(f"It is {colour}'s turn! Please enter your move!: ")
            legalMoves = list(chessBoard.legal_moves)
            for move in legalMoves:
                if str(move) == candidateMove:
                    legalMoveMade = True
                    selectedMove = candidateMove
                    break

            if not legalMoveMade:
                print("The move that you have selected is illegal! Please re-enter your move!")

        return selectedMove

    def _engineMoveInfo(self, colour):
        print(f"It is the {colour} robots turn to move. It will take around {self._maxSearchTimeSeconds} seconds to select its move.")


