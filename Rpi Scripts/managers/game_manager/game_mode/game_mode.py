from abc import ABC, abstractmethod
from chess_adversarial_search.minimax_alpha_beta import timeBoundedMinimaxAlphaBetaSearch
import chess

class GameMode(ABC):
    def __init__(self, boardManager, userInterface, maxSearchTimeSeconds):
        self._boardManager = boardManager
        self._userInterface = userInterface
        self._maxSearchTimeSeconds = maxSearchTimeSeconds
        self._maxSearchPlyDepth = 1000
        self._chessColourAsText = ['Black', 'White']


    @abstractmethod
    def playGameMode(self, chessBoard, game):
        pass

    def selectDifficulty(self):
        acceptableDifficulties = {'1', '2', '3', '4', '5', '6'}
        while True:
            difficulty = self._userInterface.selectDifficulty()

            if difficulty not in acceptableDifficulties:
                self._userInterface.displayText("You have selected an invalid difficulty level! Please Reselect!\n")
                continue

            if int(difficulty) >= 1 and int(difficulty) <= 5:
                self._maxSearchPlyDepth = int(difficulty) + 1
            break

    def endOfGame(self, chessBoard):
        self.__gameResultInfo(chessBoard)
        self._boardManager.gameEndMessage()
        self._boardManager.resetBoard()

    def _playerMove(self, chessBoard):
        # Here we will spool up the camera and pose detection
        self.__moveInfo(chessBoard)
        if self.__claimDraw(chessBoard):
            return True
        playerMove = chess.Move.from_uci(self.__playerSelectMove(chessBoard))
        # Here we will free up the camera and the pose detection resources
        self._boardManager.executeMove(playerMove, chessBoard)
        chessBoard.push(playerMove)
        self.__resultingMoveInfo(chessBoard, playerMove)
        if chessBoard.is_game_over():
            return True
        return False

    def _engineMove(self, chessBoard, game):
        # Here we will spool up the camera and pose detection
        self.__moveInfo(chessBoard)
        engineMove = timeBoundedMinimaxAlphaBetaSearch(game=game,
                                                       chessBoard=chessBoard,
                                                       maxSearchTimeSeconds=self._maxSearchTimeSeconds,
                                                       maxSearchPlyDepth=self._maxSearchPlyDepth)
        # Here we will free up the camera and the pose detection resources
        self._boardManager.executeMove(engineMove, chessBoard)
        chessBoard.push(engineMove)
        self.__resultingMoveInfo(chessBoard, engineMove)
        if chessBoard.is_game_over():
            return True
        return False
    #######################################################
    #######################################################
    #######################################################
    #######################################################
    #######################################################
    def __playerSelectMove(self, chessBoard):
        selectedMove = None
        legalMoveMade = False
        while not legalMoveMade:
            candidateMove = self._userInterface.playerSelectMove()
            availableMoves = list(chessBoard.legal_moves)
            legalMoves = []

            # Checks if the player selected promotion is supported
            for move in availableMoves:
                if (move.promotion) and (self._boardManager.promotionIsIllegal(move)):
                    continue
                legalMoves.append(move)

            for move in legalMoves:
                if str(move) == candidateMove:
                    legalMoveMade = True
                    selectedMove = candidateMove
                    break

            if not legalMoveMade:
                self._userInterface.displayText("The move that you have selected is illegal OR there is not enough material for the promotion requested! Please re-enter your move!")

        return selectedMove

    def __claimDraw(self, chessBoard):
        while chessBoard.can_claim_draw():
            if chessBoard.can_claim_fifty_moves():
                selection = self._userInterface.yesOrNoQuestion("It has been 50 consecutive moves without a capture or pawn move would you like to claim a draw?")
            else:
                selection = self._userInterface.yesOrNoQuestion("The exact same three positions have occurred during the game! Would you like to claim a draw?")

            if selection == "NO":
                return False
            elif selection == "YES":
                return True
            else:
                self._userInterface.displayText("The selection was not recognized. Please re-enter your selection!")

        return False

    def __moveInfo(self, chessBoard):
        self._userInterface.displayText(f"%%%%%%%%%%%%%%%%%%%%%%%\nIt is {self._chessColourAsText[chessBoard.turn]} turn to move.The state of the board is:\n{chessBoard}")

    def __resultingMoveInfo(self, chessBoard, move):
        self._userInterface.displayText(f"The move made was {move}.\nThe state of the board after this move is:\n{str(chessBoard)}\n%%%%%%%%%%%%%%%%%%%%%%%")

    def __gameResultInfo(self, chessBoard):
        resultStr = chessBoard.result()
        if resultStr == '1-0':
            # White wins
            self._userInterface.displayText("White Wins!\n\n\n")
        elif resultStr == '0-1':
            # Black wins
            self._userInterface.displayText("Black Wins!\n\n\n")
        else:
            self._userInterface.displayText("The game is drawn!\n\n\n")
    #######################################################
    #######################################################
    #######################################################
    #######################################################
    #######################################################


class WhitePlayerBlackRobot(GameMode):
    def playGameMode(self, chessBoard, game):
        while True:
            if self._playerMove(chessBoard):
                break

            if self._engineMove(chessBoard, game):
                break

class BlackPlayerWhiteRobot(GameMode):
    def playGameMode(self, chessBoard, game):
        while True:
            if self._engineMove(chessBoard, game):
                break

            if self._playerMove(chessBoard):
                break

class PlayerPlayer(GameMode):
    def playGameMode(self, chessBoard, game):
        while True:
            if self._playerMove(chessBoard):
                break

            if self._playerMove(chessBoard):
                break

    def selectDifficulty(self):
        return None

class RobotRobot(GameMode):
    def playGameMode(self, chessBoard, game):
        while True:
            if self._engineMove(chessBoard, game):
                break

            if self._engineMove(chessBoard, game):
                break