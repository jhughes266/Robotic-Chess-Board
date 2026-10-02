from config import *
import chess
from console_debug_info import ConsoleDebugInfo
from managers.game_manager.game_manager import GameManager
from managers.board_manager.board_manager import BoardManager
from managers.wifi_communication.communication_manager import PicoCommunicationManager, CommunicationManager
from managers.game_manager.user_interface.user_interface import *



if __name__ == '__main__':
    
    # Initiating objects depending on setting that were entered in the config
    if GAME_LOCATION == "default":
        communicationManager = CommunicationManager()
    elif GAME_LOCATION == "board":
        communicationManager = PicoCommunicationManager()

    if USER_INTERFACE_TYPE == "default":
        userInterface = TextUserInterface()
    elif USER_INTERFACE_TYPE == "stylus":
        if SCREEN_TYPE == "default":
            screens = PillowComputerScreens()
        elif SCREEN_TYPE == "oled":
            pass
        
        userInterface = StylusUserInterface(screens=screens)
    
    
    ConsoleDebugInfo.consoleOutputEnabled(enable=True)
    
    communicationManager.connectToPico()
    boardManager = BoardManager(communicationManager=communicationManager)
    gameManager = GameManager(boardManager=boardManager, userInterface=userInterface, maxSearchTimeSeconds=15)
    while gameManager.startOrQuit():
        gameManager.selectMode()
        gameManager.selectDifficulty()
        gameManager.playGame()

    communicationManager.disconnectFromPico()

    print("Thanks for playing!")

