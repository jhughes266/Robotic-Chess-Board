from abc import ABC, abstractmethod
from managers.game_manager.user_interface.stylus_triangulation.stylus_triangulator import *
from managers.game_manager.user_interface.ui_canvas import *
from screens import *
import statistics
from statistics import mode
import time
import os
class UserInterface(ABC):
    def __init__(self, boardManager):
        self._boardManager = boardManager
        self._chessColourAsText = ['Black', 'White']
    
    def prepareForUserInput(self):
        pass
    
    def finishedWithUserInput(self):
        pass

    def tearDown(self):
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

    def displayText(self, text):
        print(text)

    def yesOrNoQuestion(self, question):
        question += "\nEnter NO or YES:\nSelection: "
        return input(question)

    def getDifficultyFromUser(self):
        return input(f"Please select a difficulty from the following list:\n1: Very Easy (2 ply depth)\n2: Easy(3 ply depth)\n3: Medium (4 ply depth)\n4: Hard (5 ply depth)\n5: Very Hard (6 ply depth)\n6: Extreme (Will search to whatever depth it can within maximum search time!)\n(Please note that irrespective of the difficulty the game will search for at most the maximum search time.)\nSelection: ")

    def gameEntryPrompt(self):
        return input("Enter 0 to quit the game or 1 to start the game!\nSelection: ")

    def getGameModeFromUser(self):
        return input("Select game mode!\n1: White human player vs black robot\n2: Black human player vs white robot\n3: Human vs human\n4: Robot vs Robot \nSelection : ")

class StylusUserInterface(UserInterface):
    def __init__(self, boardManager, screens):
        super().__init__(boardManager)
        self.__gameBoardOriginPositionInRealWorld = np.array([-42, -85, 216])
        self.__moveSelectCanvas = MoveSelectCanvas(screens=screens)
        self.__gameEntryCanvas = GameEntryCanvas(screens=screens)
        self.__yesNoCanvas = YesNoCanvas(screens=screens)
        self.__difficultySelectCanvas = DifficultySelectCanvas(screens=screens)
        self.__gameModeCanvas = GameModeCanvas(screens=screens)
        self.__textMessageCanvas = TextMessageCanvas(screens=screens)
        
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

    def tearDown(self):
        pass

    def getMoveFromUser(self, displayScreen):
        originSquare = None
        destinationSquare = None
        selectedSquare = None
        selectedSquareList = []
        confirmButtonText = "Confirm\nOrigin"
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            stylusGameBoardLocation = self.__getStylusInfo()
            
            if self.__moveSelectCanvas.resetButton.isClicked(stylusGameBoardLocation):
                originSquare = None
                destinationSquare = None
                selectedSquare = None
                selectedSquareList = []
                confirmButtonText = "Confirm\nOrigin"
                
                
            candidateSquare = self.__moveSelectCanvas.findClickedSquare(stylusGameBoardLocation)
            if candidateSquare is not None:
                if len(selectedSquareList) < 5:
                    selectedSquareList.append(candidateSquare)
                else:
                    selectedSquareList.pop(0)
                    selectedSquareList.append(candidateSquare)
                    
                selectedSquare = mode(selectedSquareList)
            else:
                selectedSquareList = []

 
                    
            if self.__moveSelectCanvas.confirmButton.isClicked(stylusGameBoardLocation) and selectedSquare is not None:
                
                if originSquare is None:
                    originSquare = selectedSquare
                    selectedSquareList = []
                    selectedSquare = None
                    confirmButtonText = "Confirm\nMove"
                else:
                    destinationSquare = selectedSquare
                    return originSquare + destinationSquare
                    
            
            self.__moveSelectCanvas.draw(confirmButtonOverideText=confirmButtonText,
                                         selectedSquare=selectedSquare,
                                         originSquare=originSquare,
                                         destinationSquare=destinationSquare,
                                         displayScreen=displayScreen)
            if stylusGameBoardLocation is not None:
                self.__moveSelectCanvas.drawMouse(stylusGameBoardLocation, displayScreen=displayScreen)
            self.__moveSelectCanvas.display(displayScreen=displayScreen)

    def displayText(self, displayScreen, text):
        self.__textMessageCanvas.draw(text=text, displayScreen=displayScreen)
        self.__textMessageCanvas.display(displayScreen=displayScreen)

    def yesOrNoQuestion(self, displayScreen, question):
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            stylusGameBoardLocation = self.__getStylusInfo()

            if self.__yesNoCanvas.yesButton.isClicked(stylusGameBoardLocation):
                return "YES"
            if self.__yesNoCanvas.noButton.isClicked(stylusGameBoardLocation):
                return "NO"
            
            self.__yesNoCanvas.draw(displayScreen=displayScreen, yesNoQuestion=question)
            if stylusGameBoardLocation is not None:
                self.__yesNoCanvas.drawMouse(stylusGameBoardLocation, displayScreen=displayScreen)
            self.__yesNoCanvas.display(displayScreen=displayScreen)

    def getDifficultyFromUser(self, displayScreen):
        
        difficultySelected = '1'
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            stylusGameBoardLocation = self.__getStylusInfo()

            if self.__difficultySelectCanvas.difficulty1Button.isClicked(stylusGameBoardLocation):
                difficultySelected = '1'
            if self.__difficultySelectCanvas.difficulty2Button.isClicked(stylusGameBoardLocation):
                difficultySelected = '2'
            if self.__difficultySelectCanvas.difficulty3Button.isClicked(stylusGameBoardLocation):
                difficultySelected = '3'
            if self.__difficultySelectCanvas.difficulty4Button.isClicked(stylusGameBoardLocation):
                difficultySelected = '4'
            if self.__difficultySelectCanvas.difficulty5Button.isClicked(stylusGameBoardLocation):
                difficultySelected = '5'
            if self.__difficultySelectCanvas.difficulty6Button.isClicked(stylusGameBoardLocation):
                difficultySelected = '6'
            if self.__difficultySelectCanvas.confirmButton.isClicked(stylusGameBoardLocation):
                return difficultySelected
            
            
            self.__difficultySelectCanvas.draw(difficultySelected, displayScreen=displayScreen)
            if stylusGameBoardLocation is not None:
                self.__difficultySelectCanvas.drawMouse(stylusGameBoardLocation, displayScreen=displayScreen)
            self.__difficultySelectCanvas.display(displayScreen=displayScreen)
    
    def gameEntryPrompt(self, displayScreen):

        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            stylusGameBoardLocation = self.__getStylusInfo()

            if self.__gameEntryCanvas.startButton.isClicked(stylusGameBoardLocation):
                return 1
            elif self.__gameEntryCanvas.quitButton.isClicked(stylusGameBoardLocation):
                return 0
            
            self.__gameEntryCanvas.draw(displayScreen=displayScreen)
            if stylusGameBoardLocation is not None:
                self.__gameEntryCanvas.drawMouse(stylusGameBoardLocation, displayScreen=displayScreen)
            self.__gameEntryCanvas.display(displayScreen=displayScreen)

    def getGameModeFromUser(self, displayScreen):
        modeSelected = '1'
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            stylusGameBoardLocation = self.__getStylusInfo()

            if self.__gameModeCanvas.mode1Button.isClicked(stylusGameBoardLocation):
                modeSelected = '1'
            if self.__gameModeCanvas.mode2Button.isClicked(stylusGameBoardLocation):
                modeSelected = '2'
            if self.__gameModeCanvas.mode3Button.isClicked(stylusGameBoardLocation):
                modeSelected = '3'
            if self.__gameModeCanvas.mode4Button.isClicked(stylusGameBoardLocation):
                modeSelected = '4'
            if self.__gameModeCanvas.confirmButton.isClicked(stylusGameBoardLocation):
                return modeSelected
            
            self.__gameModeCanvas.draw(mode=modeSelected, displayScreen=displayScreen)
            if stylusGameBoardLocation is not None:
                self.__moveSelectCanvas.drawMouse(stylusGameBoardLocation, displayScreen=displayScreen)
            self.__gameModeCanvas.display(displayScreen=displayScreen)

        

screens = PillowComputerScreens()
screens.setUp()
stylusUserInterface = StylusUserInterface(boardManager=None, screens=screens)
stylusUserInterface.prepareForUserInput()
print("Get move from user")
stylusUserInterface.getMoveFromUser(displayScreen=["Black"])
time.sleep(5)
print("Display text")
stylusUserInterface.displayText(displayScreen=["White", "Black"], text="Hello\nWorld")
time.sleep(5)
print("Yes no question")
stylusUserInterface.yesOrNoQuestion(displayScreen=[ "Black"], question="Test\nquestion?")
time.sleep(5)
print("Get difficulty")
stylusUserInterface.getDifficultyFromUser(displayScreen=["Black"])
time.sleep(5)
print("Game entry")
stylusUserInterface.gameEntryPrompt(displayScreen=["Black"])
time.sleep(5)
print("Game mode from user")
stylusUserInterface.getGameModeFromUser(displayScreen=["Black"])

stylusUserInterface.finishedWithUserInput()
screens.tearDown()
