import chess
from chess_adversarial_search.game import Game
from managers.game_manager.game_mode.game_mode import *


class GameManager:
    def __init__(self, boardManager, userInterface, maxSearchTimeSeconds):
        self._boardManager = boardManager
        self._userInterface = userInterface
        self._maxSearchTimeSeconds = maxSearchTimeSeconds
        self._gameMode = None

    def startOrQuit(self):
        acceptableSelection = {'0', '1'}
        while True:
            selection = self._userInterface.gameEntryPrompt()

            if selection in acceptableSelection:
                if selection == '0':
                    return False
                else:
                    return True

            self._userInterface.displayText("Invalid selection! Please try again!\n")

    def selectMode(self):
        while True:

            selection = self._userInterface.getGameModeFromUser()

            if selection == '1':
                self._gameMode = WhitePlayerBlackRobot(boardManager=self._boardManager, userInterface=self._userInterface, maxSearchTimeSeconds=self._maxSearchTimeSeconds)
                return
            elif selection == '2':
                self._gameMode = BlackPlayerWhiteRobot(boardManager=self._boardManager, userInterface=self._userInterface, maxSearchTimeSeconds=self._maxSearchTimeSeconds)
                return
            elif selection == '3':
                self._gameMode = PlayerPlayer(boardManager=self._boardManager, userInterface=self._userInterface, maxSearchTimeSeconds=self._maxSearchTimeSeconds)
                return
            elif selection == '4':
                self._gameMode = RobotRobot(boardManager=self._boardManager, userInterface=self._userInterface, maxSearchTimeSeconds=self._maxSearchTimeSeconds)
                return

            self._userInterface.displayText("Invalid selection! Please try again!\n")

    def selectDifficulty(self):
        self._gameMode.selectDifficulty()

    def playGame(self, fen=chess.STARTING_FEN):
        chessBoard = chess.Board(fen)
        game = Game(self._boardManager)
        self._gameMode.playGameMode(chessBoard, game)
        self._gameMode.endOfGame(chessBoard)




