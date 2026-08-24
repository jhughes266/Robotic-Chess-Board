from managers.game.game_manager import GameManager
from managers.board.board_manager import BoardManager
from managers.wifi_communication.communication_manager import CommunicationManager
from managers.game.user_interface.user_interface import *


if __name__ == '__main__':
    communicationManager = CommunicationManager()
    communicationManager.connectToPico()
    boardManager = BoardManager(communicationManager=communicationManager)
    userInterface = TextUserInterface()
    gameManager = GameManager(boardManager=boardManager, userInterface=userInterface, maxSearchTimeSeconds=5)

    while gameManager.startOrQuit():
        gameManager.selectMode()
        gameManager.selectDifficulty()
        gameManager.playGame()

    communicationManager.disconnectFromPico()

    print("Thanks for playing!")

