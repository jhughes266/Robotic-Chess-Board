import chess
from chess_adversarial_search.game import Game
from chess_adversarial_search.minimax_alpha_beta import timeBoundedMinimaxAlphaBetaSearch



class BasicGameManager:
    def __init__(self, boardManager):
        self._boardManager = boardManager
        self._gameMode = None
        self._maxSearchTimeSeconds = 5
        self._maxSearchPlyDepth = 1000

    def startOrQuit(self):
        acceptableSelection = {'0', '1'}
        while True:
            selection = input("Enter 0 to quit the game or 1 to start the game!\nSelection: ")

            if selection in acceptableSelection:
                if selection == '0':
                    return False
                else:
                    return True

            print("Invalid selection! Please try again!\n")

    def selectMode(self):
        acceptableModes = {'1', '2', '3', '4'}
        while True:
            self._gameMode = '1'
            self._gameMode = input(
                "Select game mode!\n1: White human player vs black robot\n2: Black human player vs black white\n3: Human vs human\n4: Robot vs Robot \nSelection : ")

            if self._gameMode in acceptableModes:
                break

            print("Invalid selection! Please try again!\n")

    def selectDifficulty(self):
        validGameModes = ['1', '2', '4']
        acceptableDifficulties = {'1', '2', '3', '4', '5', '6'}
        while True:
            if self._gameMode in validGameModes:
                difficulty = '1'
                difficulty = input(f"Please select a difficulty from the following list:\n1: Very Easy (2 ply depth)\n2: Easy(3 ply depth)\n3: Medium (4 ply depth)\n4: Hard (5 ply depth)\n5: Very Hard (6 ply depth)\n6: Extreme (Will search to whatever depth it can within {self._maxSearchTimeSeconds} seconds)\n(Please note that irrespective of the difficulty the game will search for at most {self._maxSearchTimeSeconds} seconds.)\nSelection: ")

                if difficulty not in acceptableDifficulties:
                    print("You have selected an invalid difficulty level! Please Reselect!\n")
                    continue

                if int(difficulty) >= 1 and int(difficulty) <= 5:
                    self._maxSearchPlyDepth = int(difficulty) + 1
            break

    def playGame(self):
        chessBoard = chess.Board()
        game = Game(boardManager=self._boardManager)
        print(f"The initial board state is:\n{str(chessBoard)}\n---------------------------------------")
        while True:

            if self._gameMode == '1':
                if self._claimDraw(chessBoard):
                    break
                playerMove = self._selectMove("white", chessBoard)
                playerMove = chess.Move.from_uci(playerMove)
                self._boardManager.executeMove(playerMove, chessBoard)
                chessBoard.push(playerMove)
                self._resultingMoveInfo("white", playerMove, chessBoard)
                if chessBoard.is_game_over():
                    break

                self._engineMoveInfo("black")
                engineMove = timeBoundedMinimaxAlphaBetaSearch(game, chessBoard, maxSearchTimeSeconds=self._maxSearchTimeSeconds, maxSearchPlyDepth=self._maxSearchPlyDepth)
                self._boardManager.executeMove(engineMove, chessBoard)
                chessBoard.push(engineMove)
                self._resultingMoveInfo("black", engineMove, chessBoard)
                if chessBoard.is_game_over():
                    break


            elif self._gameMode == '2':
                self._engineMoveInfo("white")
                engineMove = timeBoundedMinimaxAlphaBetaSearch(game, chessBoard, maxSearchTimeSeconds=self._maxSearchTimeSeconds, maxSearchPlyDepth=self._maxSearchPlyDepth)
                self._boardManager.executeMove(engineMove, chessBoard)
                chessBoard.push(engineMove)
                self._resultingMoveInfo("white", engineMove, chessBoard)
                if chessBoard.is_game_over():
                    break

                if self._claimDraw(chessBoard):
                    break
                playerMove = self._selectMove("black", chessBoard)
                playerMove = chess.Move.from_uci(playerMove)
                self._boardManager.executeMove(playerMove, chessBoard)
                chessBoard.push(playerMove)
                self._resultingMoveInfo("black", playerMove, chessBoard)
                if chessBoard.is_game_over():
                    break

            elif self._gameMode == '3':
                if self._claimDraw(chessBoard):
                    break
                playerMove = self._selectMove("white", chessBoard)
                playerMove = chess.Move.from_uci(playerMove)
                self._boardManager.executeMove(playerMove, chessBoard)
                chessBoard.push(playerMove)
                self._resultingMoveInfo("white", playerMove, chessBoard)
                if chessBoard.is_game_over():
                    break

                if self._claimDraw(chessBoard):
                    break
                playerMove = self._selectMove("black", chessBoard)
                playerMove = chess.Move.from_uci(playerMove)
                self._boardManager.executeMove(playerMove, chessBoard)
                chessBoard.push(playerMove)
                self._resultingMoveInfo("black", playerMove, chessBoard)
                if chessBoard.is_game_over():
                    break

            elif self._gameMode == '4':
                self._engineMoveInfo("white")
                engineMove = timeBoundedMinimaxAlphaBetaSearch(game, chessBoard, maxSearchTimeSeconds=self._maxSearchTimeSeconds, maxSearchPlyDepth=self._maxSearchPlyDepth)
                self._boardManager.executeMove(engineMove, chessBoard)
                chessBoard.push(engineMove)
                self._resultingMoveInfo("white", engineMove, chessBoard)
                if chessBoard.is_game_over():
                    break

                self._engineMoveInfo("black")
                engineMove = timeBoundedMinimaxAlphaBetaSearch(game, chessBoard, maxSearchTimeSeconds=self._maxSearchTimeSeconds, maxSearchPlyDepth=self._maxSearchPlyDepth)
                self._boardManager.executeMove(engineMove, chessBoard)
                chessBoard.push(engineMove)
                self._resultingMoveInfo("black", engineMove, chessBoard)
                if chessBoard.is_game_over():
                    break

        self._resultInfo(chessBoard)
        self._boardManager.gameEndMessage()
        self._boardManager.resetBoard()


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

    def _claimDraw(self, chessBoard):

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

    def _engineMoveInfo(self, colour):
        print(f"It is the {colour} robots turn to move. It will take at most around {self._maxSearchTimeSeconds} seconds to select its move.")

    def _resultingMoveInfo(self, colour, move, chessBoard):
        print(f"---------------------------------------\nThe {colour} players move was {move}.\nThe state of the board after this move is:\n{str(chessBoard)}\n---------------------------------------")

    def _resultInfo(self, chessBoard):
        resultStr = chessBoard.result()
        if resultStr == '1-0':
            # White wins
            print("White Wins!\n\n\n")
        elif resultStr == '0-1':
            # Black wins
            print("Black Wins!\n\n\n")
        else:
            print("The game is drawn!\n\n\n")




