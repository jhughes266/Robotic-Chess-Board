from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont
from managers.game_manager.user_interface.screen import *
from managers.game_manager.user_interface.ui_canvas_element import *
import numpy as np


class UiCanvas(ABC):
    def __init__(self, screen):
        self._screen = screen
        self.mouse = Mouse(elementId="Mouse", screen=screen)

    @abstractmethod
    def draw(self):
        pass
    
    def display(self):
        self._screen.display()
    
    def drawMouse(self, stylusGameBoardLocation):
        self.mouse.draw(stylusGameBoardLocation)

class TextMessageCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.text = Text(elementId="text",
                         screenLocation=(0, 0),
                         screen=self._screen,
                         fontSize=10)

    def draw(self, text=None):
        self.text.draw(text)

class YesNoCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.yesButton = Button(elementId="yesButton",
                                screenLocation=(0, 51),
                                screen=screen,
                                pixelHeight=13,
                                pixelWidth=64,
                                textElement="YES")

        self.noButton = Button(elementId="noButton",
                               screenLocation=(64, 51),
                               screen=screen,
                               pixelHeight=13,
                               pixelWidth=64,
                               textElement="NO")

        self.text = Text(elementId="yesNoSelection",
                         screenLocation=(0, 0),
                         screen=self._screen)

    def draw(self, yesNoQuestion=None):
        self.yesButton.draw()
        self.noButton.draw()
        self.text.draw(text=yesNoQuestion)

class GameEntryCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.quitButton = Button(elementId="quitButton",
                                 screenLocation=(0,32),
                                 screen=screen,
                                 pixelHeight=32,
                                 pixelWidth=128,
                                 textElement="QUIT")
        
        self.startButton = Button(elementId="startButton",
                                  screenLocation=(0,0),
                                  screen=screen,
                                  pixelHeight=32,
                                  pixelWidth=128,
                                  textElement="START")

    def draw(self):
        self.quitButton.draw()
        self.startButton.draw()

class DifficultySelectCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        difficultyButtonFontSize = 14
        self.difficulty1Button = Button(elementId="difficulty1",
                                        screenLocation=(0,0),
                                        screen=screen,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="1",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty2Button = Button(elementId="difficulty2",
                                        screenLocation=(21,0),
                                        screen=screen,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="2",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty3Button = Button(elementId="difficulty3",
                                        screenLocation=(0,21),
                                        screen=screen,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="3",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty4Button = Button(elementId="difficulty4",
                                        screenLocation=(21,21),
                                        screen=screen,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="4",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty5Button = Button(elementId="difficulty5",
                                        screenLocation=(0,42),
                                        screen=screen,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="5",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty6Button = Button(elementId="difficulty6",
                                        screenLocation=(21,42),
                                        screen=screen,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="6",
                                        fontSize=difficultyButtonFontSize)

        self.confirmButton = Button(elementId="confirm",
                                    screenLocation=(64,46),
                                    screen=screen,
                                    pixelHeight=17,
                                    pixelWidth=64,
                                    textElement="CONFIRM")

        self.currentDifficultyText = Text(elementId="CurrentDifficulty",
                                          screenLocation=(96, 5),
                                          screen=self._screen,
                                          anchor="mm")

        self.__buttonList = [self.difficulty1Button,
                             self.difficulty2Button,
                             self.difficulty3Button,
                             self.difficulty4Button,
                             self.difficulty5Button,
                             self.difficulty6Button,
                             self.confirmButton]

        self.difficultyImage = PastedImage(elementId="DifficultyImage",
                                           screenLocation=(64, 11),
                                           screen=self._screen)

        #load in all the difficulty images into an easy to access dictionary
        self.__difficultyImages = {
            '1':Image.open("ui_images/pawn.jpg"),
            '2':Image.open("ui_images/knight.jpg"),
            '3':Image.open("ui_images/bishop.jpg"),
            '4':Image.open("ui_images/rook.jpg"),
            '5':Image.open("ui_images/queen.jpg"),
            '6':Image.open("ui_images/king.jpg"),
        }


    def draw(self, difficulty):
        for button in self.__buttonList:
            button.draw()
        self.currentDifficultyText.draw(difficulty)
        self.difficultyImage.draw(self.__difficultyImages[difficulty])

class MoveSelectCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.__files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.__ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.__chessBoardButtonArray = self.__constructChessBoardButtonArray()
        self.__fileAndRankTextArray = self.__constructFileAndRankTextArray()
        self.confirmButton = Button(elementId="confirmButton",
                                    screenLocation=(77,1),
                                    screen=screen,
                                    pixelHeight=29,
                                    pixelWidth=50,
                                    textElement="Confirm")
        
        self.resetButton = Button(elementId="resetButton",
                                  screenLocation=(77,49),
                                  screen=screen,
                                  pixelHeight=15,
                                  pixelWidth=50,
                                  textElement="Reset")

        self.moveSelectInfoText = Text(elementId="Move Selection Info",
                                       screenLocation=(100, 39),
                                       screen=screen,
                                       anchor="mm")
        
        self.originFlashingRectangle = FlashingRectangle(elementId="Origin Select",
                                                         screen=screen,
                                                         screenLocation=(82, 31),
                                                         pixelHeight=17,
                                                         pixelWidth=17)
        
        self.destinationFlashingRectangle = FlashingRectangle(elementId="Destination Select",
                                                              screen=screen,
                                                              screenLocation=(105, 31),
                                                              pixelHeight=17,
                                                              pixelWidth=17)
        
    def __constructChessBoardButtonArray(self):
        chessBoardButtonArray = []

        pixelSideLength = 8
        lengthAfterOverLap = pixelSideLength - 1

        screenPixelHeight = 64
        xPixelOffsetFromBottomLeft = 0
        yPixelOffsetFromBottomLeft = 0
        fill = 0
        for xIdx, file in enumerate(self.__files):
            for yIdx, rank in enumerate(self.__ranks):
                xScreenLocation = xIdx * (lengthAfterOverLap)
                yScreenLocation = (screenPixelHeight - pixelSideLength) - (yIdx * lengthAfterOverLap)
                xScreenLocation += xPixelOffsetFromBottomLeft
                yScreenLocation += yPixelOffsetFromBottomLeft
                
                button = Button(elementId=file+rank,
                                screenLocation=(xScreenLocation, yScreenLocation),
                                screen=self._screen,
                                pixelHeight=pixelSideLength,
                                pixelWidth=pixelSideLength,
                                textElement="",
                                fill=fill)
                
                chessBoardButtonArray.append(button)
                #alternate the fill each time to get the checkerboard pattern
                fill = int(not(fill))
            #need to alternate again to ensure checkerboard pattern and not stipes
            fill = int(not (fill))
        return chessBoardButtonArray

    def __constructFileAndRankTextArray(self):
        fileAndRankTextArray = []
        screenPixelHeight = 64
        xPixelOffsetFromBottomLeftRank = 3
        yPixelOffsetFromBottomLeftRank = -64
        xPixelOffsetFromBottomLeftFile = 58
        yPixelOffsetFromBottomLeftFile = -8
        spacing = 7
        for xIdx, file in enumerate(self.__files):
            text = Text(elementId=file,
                        screenLocation=(xPixelOffsetFromBottomLeftRank + xIdx * spacing, screenPixelHeight + yPixelOffsetFromBottomLeftRank),
                        screen=self._screen,
                        fontSize=5)
            fileAndRankTextArray.append(text)

        for yIdx, rank in enumerate(self.__ranks):
            text = Text(elementId=rank,
                        screenLocation=(xPixelOffsetFromBottomLeftFile,screenPixelHeight + yPixelOffsetFromBottomLeftFile - yIdx * spacing),
                        screen=self._screen,
                        fontSize=7)
            fileAndRankTextArray.append(text)

        return fileAndRankTextArray


    def findClickedSquare(self, stylusGameBoardLocation):
        clickedSquare = None
        for button in self.__chessBoardButtonArray:
            if button.isClicked(stylusGameBoardLocation):
                clickedSquare = button.elementId
        return clickedSquare

    def draw(self, confirmButtonOverideText, selectedSquare, originSquare, destinationSquare, info=""):
        for button in self.__chessBoardButtonArray:
            button.draw()

        for text in self.__fileAndRankTextArray:
            text.draw()


        self.confirmButton.draw(textOveride=confirmButtonOverideText)
        self.resetButton.draw()
        
        move = "         ->   "
        if selectedSquare is not None:
            if originSquare is None:
                move = selectedSquare + "   ->  "
            else:
                move = originSquare + " -> " + selectedSquare
        elif originSquare is not None:
             move = originSquare + " ->        "
            
            
        if originSquare is None:
            self.originFlashingRectangle.draw()
        else:
            self.destinationFlashingRectangle.draw()
        
        self.moveSelectInfoText.draw(move)


class GameModeCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.mode1Button = Button(elementId="mode1",
                                  screenLocation=(0,0),
                                  screen=screen,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="1")

        self.mode2Button = Button(elementId="mode2",
                                  screenLocation=(32,0),
                                  screen=screen,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="2")

        self.mode3Button = Button(elementId="mode3",
                                  screenLocation=(0,32),
                                  screen=screen,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="3")

        self.mode4Button = Button(elementId="mode4",
                                  screenLocation=(32,32),
                                  screen=screen,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="4")

        self.confirmButton = Button(elementId="confirm",
                                    screenLocation=(70,40),
                                    screen=screen,
                                    pixelHeight=19,
                                    pixelWidth=52,
                                    textElement="Confirm")

        self.currentGameModeText = Text(elementId="currentGameMode",
                                        screenLocation=(65, 0),
                                        screen=self._screen,
                                        fontSize=9)
        self.__gameModeNumberToText = {
            "1" : "White human\nvs\nBlack robot",
            "2" : "Black human\nvs\nWhite robot",
            "3" : "Human\nvs\nHuman",
            "4" : "Robot\nvs\nRobot" 
            }

    def draw(self, mode):
        self.mode1Button.draw()
        self.mode2Button.draw()
        self.mode3Button.draw()
        self.mode4Button.draw()
        self.confirmButton.draw()
        self.currentGameModeText.draw(self.__gameModeNumberToText[mode])

