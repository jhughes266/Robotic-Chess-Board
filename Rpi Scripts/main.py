from managers.game.basic_game_manager import BasicGameManager
from managers.board.basic_board_manager import BasicBoardManager
from managers.wifi_communication.basic_communication_manager import BasicCommunicationManager

if __name__ == '__main__':
    basicCommunicationManager = BasicCommunicationManager()
    basicBoardManager = BasicBoardManager(communicationManager=basicCommunicationManager)
    gameManager = BasicGameManager(boardManager=basicBoardManager)

    while gameManager.startOrQuit():
        basicCommunicationManager.connectToPico()
        gameManager.selectMode()
        gameManager.selectDifficulty()
        gameManager.playGame()

    print("Thanks for playing!")

