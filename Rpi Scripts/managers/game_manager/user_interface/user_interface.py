from abc import ABC, abstractmethod
from managers.game_manager.user_interface.stylus_triangulation.stylus_triangulator import *
from managers.game_manager.user_interface.ui_canvas import *
import statistics
from statistics import mode
import os
class UserInterface(ABC):
    def __init__(self, boardManager):
        self._boardManager = boardManager
        self._chessColourAsText = ['Black', 'White']
    
    def prepareForUserInput():
        pass
    
    def finishedWithUserInput():
        pass

    @abstractmethod
    def getMoveFromUser(self):
        pass

    @abstractmethod
    def displayText(self, str):
        pass

    @abstractmethod
    def yesOrNoQuestion(self, str):
        pass

    @abstractmethod
    def getDifficultyFromUser(self):
        pass

    @abstractmethod
    def gameEntryPrompt(self):
        pass

    @abstractmethod
    def getGameModeFromUser(self):
        pass

class TextUserInterface(UserInterface):    
    def getMoveFromUser(self):
        return input("Please enter your move!: ")

    def displayText(self, str):
        print(str)

    def yesOrNoQuestion(self, str):
        str += "\nEnter NO or YES:\nSelection: "
        return input(str)

    def getDifficultyFromUser(self):
        return input(f"Please select a difficulty from the following list:\n1: Very Easy (2 ply depth)\n2: Easy(3 ply depth)\n3: Medium (4 ply depth)\n4: Hard (5 ply depth)\n5: Very Hard (6 ply depth)\n6: Extreme (Will search to whatever depth it can within maximum search time!)\n(Please note that irrespective of the difficulty the game will search for at most the maximum search time.)\nSelection: ")

    def gameEntryPrompt(self):
        return input("Enter 0 to quit the game or 1 to start the game!\nSelection: ")

    def getGameModeFromUser(self):
        return input("Select game mode!\n1: White human player vs black robot\n2: Black human player vs white robot\n3: Human vs human\n4: Robot vs Robot \nSelection : ")

class StylusUserInterface(UserInterface):
    def __init__(self, boardManager):
        super().__init__(boardManager)
        self.__gameBoardOriginPositionInRealWorld = np.array([-42, -85, 216])
        self.__moveSelectCanvas = MoveSelectCanvas()
        self.__gameEntryCanvas = GameEntryCanvas()
        
    def prepareForUserInput(self):
        aCam = OpenCvDevice(captureWidth=640, captureHeight=480, deviceIndex=0)
        bCam = PiCameraDevice(captureWidth=640, captureHeight=480, deviceIndex = 0)
        self.__triangulator = StylusTriangulator(aCamObj=aCam, bCamObj=bCam,resourcesPath="stylus_triangulation/resources", aCamType='usb', bCamType='csi')
        self.__triangulator.setUp()
    
    def finishedWithUserInput(self):
        self.__triangulator.tearDown()
    
    def __getStylusInfo(self):
        stylusRealWorldLocation = self.__triangulator.run() 
        if stylusRealWorldLocation is not None:
            gameBoardLocation = self.__realWorldLocationToGameBoardLocation(stylusRealWorldLocation)
            return gameBoardLocation
    
    def __realWorldLocationToGameBoardLocation(self, realWorldLocation):
        gameBoardLocation = realWorldLocation - self.__gameBoardOriginPositionInRealWorld
        return gameBoardLocation

    def getMoveFromUser(self):
        originSquare = None
        destinationSquare = None
        selectedSquareList = []
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            stylusGameBoardLocation = self.__getStylusInfo()
            if self.__moveSelectCanvas.confirmButton.isClicked(stylusGameBoardLocation):
                if originSquare is not None and destinationSquare is not None:
                    return originSquare + destinationSquare
                else:
                    print("Please Select a destination and an origin!")
                
            if self.__moveSelectCanvas.resetButton.isClicked(stylusGameBoardLocation):
                originSquare = None
                destinationSquare = None
                print("Selection Reset!")
            
            
            candidateSquare = self.__moveSelectCanvas.findClickedSquare(stylusGameBoardLocation)
            if candidateSquare is None and len(selectedSquareList) == 0:
                continue
            elif candidateSquare is not None:
                selectedSquareList.append(candidateSquare)
                continue
            elif candidateSquare is None and len(selectedSquareList) > 0:
                selectedSquare = mode(selectedSquareList)
                selectedSquareList = []
                
                if originSquare is None:
                    originSquare = selectedSquare
                    print(f"origin is : {originSquare}")
                elif originSquare is not None:
                    destinationSquare = selectedSquare
                    print(f"destination is : {destinationSquare}")
                
            
                
                
            
            
    def displayText(self, str):
        pass

    def yesOrNoQuestion(self, str):
        pass

    def getDifficultyFromUser(self):
        pass

    def gameEntryPrompt(self):
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            stylusGameBoardLocation = self.__getStylusInfo()

            if self.__gameEntryCanvas.startButton.isClicked(stylusGameBoardLocation):
                return 1
            if self.__gameEntryCanvas.quitButton.isClicked(stylusGameBoardLocation):
                return 0
            
            
        

    def getGameModeFromUser(self):
        pass
    
        
test = StylusUserInterface(None)
test.prepareForUserInput()
print(test.getMoveFromUser())
test.finishedWithUserInput()
