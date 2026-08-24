from managers.game.game_manager import GameManager
from managers.board.board_manager import BoardManager
from managers.wifi_communication.basic_communication_manager import BasicCommunicationManager
from managers.game.user_interface.user_interface import *


if __name__ == '__main__':
    basicCommunicationManager = BasicCommunicationManager()
    boardManager = BoardManager(communicationManager=basicCommunicationManager)
    userInterface = TextUserInterface()
    gameManager = GameManager(boardManager=boardManager, userInterface=userInterface, maxSearchTimeSeconds=5)

    while gameManager.startOrQuit():
        basicCommunicationManager.connectToPico()
        gameManager.selectMode()
        gameManager.selectDifficulty()
        gameManager.playGame()

    print("Thanks for playing!")

