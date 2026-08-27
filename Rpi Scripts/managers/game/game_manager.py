import chess
from chess_adversarial_search.game import Game
from managers.game.game_mode.game_mode import *


class GameManager:
    def __init__(self, boardManager, userInterface, maxSearchTimeSeconds):
        self._boardManager = boardManager
        self._userInterface = userInterface
        self._maxSearchTimeSeconds = maxSearchTimeSeconds
        self._gameMode = None

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
        while True:

            selection = input("Select game mode!\n1: White human player vs black robot\n2: Black human player vs white robot\n3: Human vs human\n4: Robot vs Robot \nSelection : ")


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

            print("Invalid selection! Please try again!\n")

    def selectDifficulty(self):
        self._gameMode.selectDifficulty()

    def playGame(self, fen=chess.STARTING_FEN):
        chessBoard = chess.Board(fen)
        game = Game(self._boardManager)
        self._gameMode.playGameMode(chessBoard, game)
        self._gameMode.endOfGame(chessBoard)




