import chess

from managers.game_manager.game_manager import GameManager
from managers.board_manager.board_manager import BoardManager
from managers.wifi_communication.communication_manager import PicoCommunicationManager, CommunicationManager
from managers.game_manager.user_interface.user_interface import *


if __name__ == '__main__':
    communicationManager = PicoCommunicationManager()
    communicationManager.connectToPico()
    boardManager = BoardManager(communicationManager=communicationManager)
    userInterface = TextUserInterface(boardManager=boardManager)
    gameManager = GameManager(boardManager=boardManager, userInterface=userInterface, maxSearchTimeSeconds=15)
    while gameManager.startOrQuit():
        gameManager.selectMode()
        gameManager.selectDifficulty()
        gameManager.playGame()

    communicationManager.disconnectFromPico()

    print("Thanks for playing!")

