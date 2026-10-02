from abc import ABC, abstractmethod
from managers.game_manager.user_interface.screens import *
from managers.game_manager.user_interface.ui_canvas_element import *


class UiCanvas(ABC):
    def __init__(self, screens):
        self._screens = screens
        self.mouse = Mouse(elementId="Mouse", screens=screens)

    @abstractmethod
    def draw(self):
        pass
    
    def display(self,displayScreen):
        self._screens.display(displayScreen=displayScreen)
    
    def drawMouse(self, stylusGameBoardLocation, displayScreen):
        self.mouse.draw(stylusGameBoardLocation, displayScreen=displayScreen)

class TextMessageCanvas(UiCanvas):
    def __init__(self, screens):
        super().__init__(screens)
        self.text = Text(elementId="text",
                         screenLocation=(0, 0),
                         screens=self._screens,
                         fontSize=10)

    def draw(self, displayScreen, text=None):
        self.text.draw(displayScreen=displayScreen, text=text)

class YesNoCanvas(UiCanvas):
    def __init__(self, screens):
        super().__init__(screens)
        self.yesButton = Button(elementId="yesButton",
                                screenLocation=(0, 51),
                                screens=screens,
                                pixelHeight=13,
                                pixelWidth=64,
                                textElement="YES")

        self.noButton = Button(elementId="noButton",
                               screenLocation=(64, 51),
                               screens=screens,
                               pixelHeight=13,
                               pixelWidth=64,
                               textElement="NO")

        self.text = Text(elementId="yesNoSelection",
                         screenLocation=(0, 0),
                         screens=self._screens)

    def draw(self, displayScreen, yesNoQuestion=None):
        self.yesButton.draw(displayScreen=displayScreen)
        self.noButton.draw(displayScreen=displayScreen)
        self.text.draw(displayScreen=displayScreen, text=yesNoQuestion)

class GameEntryCanvas(UiCanvas):
    def __init__(self, screens):
        super().__init__(screens)
        self.quitButton = Button(elementId="quitButton",
                                 screenLocation=(0,32),
                                 screens=screens,
                                 pixelHeight=32,
                                 pixelWidth=128,
                                 textElement="QUIT")
        
        self.startButton = Button(elementId="startButton",
                                  screenLocation=(0,0),
                                  screens=screens,
                                  pixelHeight=32,
                                  pixelWidth=128,
                                  textElement="START")

    def draw(self, displayScreen):
        self.quitButton.draw(displayScreen=displayScreen)
        self.startButton.draw(displayScreen=displayScreen)

class DifficultySelectCanvas(UiCanvas):
    def __init__(self, screens):
        super().__init__(screens)
        difficultyButtonFontSize = 14
        self.difficulty1Button = Button(elementId="difficulty1",
                                        screenLocation=(0,0),
                                        screens=screens,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="1",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty2Button = Button(elementId="difficulty2",
                                        screenLocation=(21,0),
                                        screens=screens,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="2",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty3Button = Button(elementId="difficulty3",
                                        screenLocation=(0,21),
                                        screens=screens,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="3",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty4Button = Button(elementId="difficulty4",
                                        screenLocation=(21,21),
                                        screens=screens,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="4",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty5Button = Button(elementId="difficulty5",
                                        screenLocation=(0,42),
                                        screens=screens,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="5",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty6Button = Button(elementId="difficulty6",
                                        screenLocation=(21,42),
                                        screens=screens,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="6",
                                        fontSize=difficultyButtonFontSize)

        self.confirmButton = Button(elementId="confirm",
                                    screenLocation=(64,46),
                                    screens=screens,
                                    pixelHeight=17,
                                    pixelWidth=64,
                                    textElement="CONFIRM")

        self.currentDifficultyText = Text(elementId="CurrentDifficulty",
                                          screenLocation=(96, 5),
                                          screens=screens,
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
                                           screens=screens)

        #load in all the difficulty images into an easy to access dictionary
        self.__difficultyImages = {
            '1':Image.open("ui_images/pawn.jpg"),
            '2':Image.open("ui_images/knight.jpg"),
            '3':Image.open("ui_images/bishop.jpg"),
            '4':Image.open("ui_images/rook.jpg"),
            '5':Image.open("ui_images/queen.jpg"),
            '6':Image.open("ui_images/king.jpg"),
        }


    def draw(self, difficulty, displayScreen):
        for button in self.__buttonList:
            button.draw(displayScreen=displayScreen)
        self.currentDifficultyText.draw(displayScreen=displayScreen, text=difficulty)
        self.difficultyImage.draw(self.__difficultyImages[difficulty], displayScreen=displayScreen)

class MoveSelectCanvas(UiCanvas):
    def __init__(self, screens):
        super().__init__(screens)
        self.__files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.__ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.__chessBoardButtonArray = self.__constructChessBoardButtonArray()
        self.__fileAndRankTextArray = self.__constructFileAndRankTextArray()
        self.confirmButton = Button(elementId="confirmButton",
                                    screenLocation=(77,1),
                                    screens=screens,
                                    pixelHeight=29,
                                    pixelWidth=50,
                                    textElement="Confirm")
        
        self.resetButton = Button(elementId="resetButton",
                                  screenLocation=(77,49),
                                  screens=screens,
                                  pixelHeight=15,
                                  pixelWidth=50,
                                  textElement="Reset")

        self.moveSelectInfoText = Text(elementId="Move Selection Info",
                                       screenLocation=(100, 39),
                                       screens=screens,
                                       anchor="mm")
        
        self.originFlashingRectangle = FlashingRectangle(elementId="Origin Select",
                                                         screens=screens,
                                                         screenLocation=(82, 31),
                                                         pixelHeight=17,
                                                         pixelWidth=17)
        
        self.destinationFlashingRectangle = FlashingRectangle(elementId="Destination Select",
                                                              screens=screens,
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
                                screens=self._screens,
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
                        screens=self._screens,
                        fontSize=5)
            fileAndRankTextArray.append(text)

        for yIdx, rank in enumerate(self.__ranks):
            text = Text(elementId=rank,
                        screenLocation=(xPixelOffsetFromBottomLeftFile,screenPixelHeight + yPixelOffsetFromBottomLeftFile - yIdx * spacing),
                        screens=self._screens,
                        fontSize=7)
            fileAndRankTextArray.append(text)

        return fileAndRankTextArray


    def findClickedSquare(self, stylusGameBoardLocation):
        clickedSquare = None
        for button in self.__chessBoardButtonArray:
            if button.isClicked(stylusGameBoardLocation):
                clickedSquare = button.elementId
        return clickedSquare

    def draw(self, confirmButtonOverideText, selectedSquare, originSquare, destinationSquare, displayScreen, info=""):
        for button in self.__chessBoardButtonArray:
            button.draw(displayScreen=displayScreen)

        for text in self.__fileAndRankTextArray:
            text.draw(displayScreen=displayScreen)


        self.confirmButton.draw(textOveride=confirmButtonOverideText, displayScreen=displayScreen)
        self.resetButton.draw(displayScreen=displayScreen)
        
        move = "         ->   "
        if selectedSquare is not None:
            if originSquare is None:
                move = selectedSquare + "   ->  "
            else:
                move = originSquare + " -> " + selectedSquare
        elif originSquare is not None:
             move = originSquare + " ->        "
            
            
        if originSquare is None:
            self.originFlashingRectangle.draw(displayScreen=displayScreen)
        else:
            self.destinationFlashingRectangle.draw(displayScreen=displayScreen)
        
        self.moveSelectInfoText.draw(displayScreen=displayScreen, text=move)


class GameModeCanvas(UiCanvas):
    def __init__(self, screens):
        super().__init__(screens)
        self.mode1Button = Button(elementId="mode1",
                                  screenLocation=(0,0),
                                  screens=screens,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="1")

        self.mode2Button = Button(elementId="mode2",
                                  screenLocation=(32,0),
                                  screens=screens,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="2")

        self.mode3Button = Button(elementId="mode3",
                                  screenLocation=(0,32),
                                  screens=screens,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="3")

        self.mode4Button = Button(elementId="mode4",
                                  screenLocation=(32,32),
                                  screens=screens,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="4")

        self.confirmButton = Button(elementId="confirm",
                                    screenLocation=(70,40),
                                    screens=screens,
                                    pixelHeight=19,
                                    pixelWidth=52,
                                    textElement="Confirm")

        self.currentGameModeText = Text(elementId="currentGameMode",
                                        screenLocation=(65, 0),
                                        screens=screens,
                                        fontSize=9)
        self.__gameModeNumberToText = {
            "1" : "White human\nvs\nBlack robot",
            "2" : "Black human\nvs\nWhite robot",
            "3" : "Human\nvs\nHuman",
            "4" : "Robot\nvs\nRobot" 
            }

    def draw(self, mode, displayScreen):
        self.mode1Button.draw(displayScreen=displayScreen)
        self.mode2Button.draw(displayScreen=displayScreen)
        self.mode3Button.draw(displayScreen=displayScreen)
        self.mode4Button.draw(displayScreen=displayScreen)
        self.confirmButton.draw(displayScreen=displayScreen)
        self.currentGameModeText.draw(displayScreen=displayScreen, text=self.__gameModeNumberToText[mode])

