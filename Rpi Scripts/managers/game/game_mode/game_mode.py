from abc import ABC, abstractmethod
from chess_adversarial_search.minimax_alpha_beta import timeBoundedMinimaxAlphaBetaSearch
import chess

class GameMode(ABC):
    def __init__(self, boardManager, userInterface, maxSearchTimeSeconds):
        self._boardManager = boardManager
        self._userInterface = userInterface
        self._maxSearchTimeSeconds = maxSearchTimeSeconds
        self._maxSearchPlyDepth = 1000

    @abstractmethod
    def playGameMode(self, chessBoard, game):
        pass

    def selectDifficulty(self):
        acceptableDifficulties = {'1', '2', '3', '4', '5', '6'}
        while True:
            difficulty = input(
                f"Please select a difficulty from the following list:\n1: Very Easy (2 ply depth)\n2: Easy(3 ply depth)\n3: Medium (4 ply depth)\n4: Hard (5 ply depth)\n5: Very Hard (6 ply depth)\n6: Extreme (Will search to whatever depth it can within {self._maxSearchTimeSeconds} seconds)\n(Please note that irrespective of the difficulty the game will search for at most {self._maxSearchTimeSeconds} seconds.)\nSelection: ")

            if difficulty not in acceptableDifficulties:
                print("You have selected an invalid difficulty level! Please Reselect!\n")
                continue

            if int(difficulty) >= 1 and int(difficulty) <= 5:
                self._maxSearchPlyDepth = int(difficulty) + 1
            break

    def endOfGame(self, chessBoard):
        self._userInterface.gameResultInfo(chessBoard)
        self._boardManager.gameEndMessage()
        self._boardManager.resetBoard()

    def _playerMove(self, chessBoard):
        self._userInterface.moveInfo(chessBoard)
        if self._userInterface.claimDraw(chessBoard):
            return True
        playerMove = chess.Move.from_uci(self._userInterface.playerSelectMove(chessBoard))
        self._boardManager.executeMove(playerMove, chessBoard)
        chessBoard.push(playerMove)
        self._userInterface.resultingMoveInfo(chessBoard, playerMove)
        if chessBoard.is_game_over():
            return True

        return False

    def _engineMove(self, chessBoard, game):
        self._userInterface.moveInfo(chessBoard)
        engineMove = timeBoundedMinimaxAlphaBetaSearch(game=game,
                                                       chessBoard=chessBoard,
                                                       maxSearchTimeSeconds=self._maxSearchTimeSeconds,
                                                       maxSearchPlyDepth=self._maxSearchPlyDepth)
        self._boardManager.executeMove(engineMove, chessBoard)
        chessBoard.push(engineMove)
        self._userInterface.resultingMoveInfo(chessBoard, engineMove)
        if chessBoard.is_game_over():
            return True

        return False

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