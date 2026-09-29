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
                                gameBoardLocation=[0, 0, 0],
                                screenLocation=(0, 51),
                                screen=screen,
                                realXLength=80,
                                realZLength=160,
                                pixelHeight=13,
                                pixelWidth=64,
                                textElement="YES")

        self.noButton = Button(elementId="noButton",
                               gameBoardLocation=[80, 0, 0],
                               screenLocation=(64, 51),
                               screen=screen,
                               realXLength=80,
                               realZLength=160,
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
                                 gameBoardLocation=[0,0,0],
                                 screenLocation=(0,32),
                                 screen=screen,
                                 realXLength=80,
                                 realZLength=240,
                                 pixelHeight=32,
                                 pixelWidth=128,
                                 textElement="QUIT")
        
        self.startButton = Button(elementId="startButton",
                                  gameBoardLocation=[80,0,0],
                                  screenLocation=(0,0),
                                  screen=screen,
                                  realXLength=80,
                                  realZLength=240,
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
                                        gameBoardLocation=[106.66, 0, 0],
                                        screenLocation=(0,0),
                                        screen=screen,
                                        realXLength=53.33,
                                        realZLength=53.33,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="1",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty2Button = Button(elementId="difficulty2",
                                        gameBoardLocation=[106.66, 0, 53.33],
                                        screenLocation=(21,0),
                                        screen=screen,
                                        realXLength=53.33,
                                        realZLength=53.33,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="2",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty3Button = Button(elementId="difficulty3",
                                        gameBoardLocation=[53.33, 0, 0],
                                        screenLocation=(0,21),
                                        screen=screen,
                                        realXLength=53.33,
                                        realZLength=53.33,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="3",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty4Button = Button(elementId="difficulty4",
                                        gameBoardLocation=[53.33, 0, 53.33],
                                        screenLocation=(21,21),
                                        screen=screen,
                                        realXLength=53.33,
                                        realZLength=53.33,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="4",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty5Button = Button(elementId="difficulty5",
                                        gameBoardLocation=[0, 0, 0],
                                        screenLocation=(0,42),
                                        screen=screen,
                                        realXLength=53.33,
                                        realZLength=53.33,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="5",
                                        fontSize=difficultyButtonFontSize)

        self.difficulty6Button = Button(elementId="difficulty6",
                                        gameBoardLocation=[0, 0, 53.33],
                                        screenLocation=(21,42),
                                        screen=screen,
                                        realXLength=53.33,
                                        realZLength=53.33,
                                        pixelHeight=21,
                                        pixelWidth=21,
                                        textElement="6",
                                        fontSize=difficultyButtonFontSize)

        self.confirmButton = Button(elementId="confirm",
                                    gameBoardLocation=[0, 0, 120],
                                    screenLocation=(64,46),
                                    screen=screen,
                                    realXLength=53.33,
                                    realZLength=120,
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
                                    gameBoardLocation=[120,0,180],
                                    screenLocation=(77,5),
                                    screen=screen,
                                    realXLength=40,
                                    realZLength=70,
                                    pixelHeight=15,
                                    pixelWidth=50,
                                    textElement="Confirm")
        
        self.resetButton = Button(elementId="resetButton",
                                  gameBoardLocation=[0,0,180],
                                  screenLocation=(77,48),
                                  screen=screen,
                                  realXLength=40,
                                  realZLength=70,
                                  pixelHeight=15,
                                  pixelWidth=50,
                                  textElement="Reset")

        self.moveSelectInfoText = Text(elementId="Move Selection Info",
                                       screenLocation=(100, 28),
                                       screen=screen,
                                       anchor="mm")

        self.generaInfoText = Text(elementId="General Info",
                                   screenLocation=(100, 41),
                                   screen=screen,
                                   fontSize=9,
                                   anchor="mm")
        
    def __constructChessBoardButtonArray(self):
        chessBoardButtonArray = []

        realSideLength = 20
        pixelSideLength = 8
        screenPixelHeight = 64
        xPixelOffsetFromBottomLeft = 0
        yPixelOffsetFromBottomLeft = 0
        fill = 0
        for zIdx, file in enumerate(self.__files):
            for xIdx, rank in enumerate(self.__ranks):
                lengthAfterOverLap = pixelSideLength - 1
                xScreenLocation = zIdx * (lengthAfterOverLap)
                yScreenLocatioj = (screenPixelHeight - pixelSideLength) - (xIdx * lengthAfterOverLap)
                xScreenLocation += xPixelOffsetFromBottomLeft
                yScreenLocatioj += yPixelOffsetFromBottomLeft
                button = Button(elementId=file+rank,
                                gameBoardLocation=[0+xIdx*realSideLength, 0, 0+zIdx*realSideLength],
                                screenLocation=(xScreenLocation, yScreenLocatioj),
                                screen=self._screen,
                                realXLength=realSideLength,
                                realZLength=realSideLength,
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
        for button in self.__chessBoardButtonArray:
            if button.isClicked(stylusGameBoardLocation):
                return button.elementId
        return None

    def draw(self, move="  ->  ", info=""):
        for button in self.__chessBoardButtonArray:
            button.draw()

        for text in self.__fileAndRankTextArray:
            text.draw()


        self.confirmButton.draw()
        self.resetButton.draw()
        self.moveSelectInfoText.draw(move)
        self.generaInfoText.draw(info)

class GameModeCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.mode1Button = Button(elementId="mode1",
                                  gameBoardLocation=[80, 0, 0],
                                  screenLocation=(0,0),
                                  screen=screen,
                                  realXLength=80,
                                  realZLength=80,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="1")

        self.mode2Button = Button(elementId="mode2",
                                  gameBoardLocation=[80, 0, 80],
                                  screenLocation=(32,0),
                                  screen=screen,
                                  realXLength=80,
                                  realZLength=80,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="2")

        self.mode3Button = Button(elementId="mode3",
                                  gameBoardLocation=[0, 0, 0],
                                  screenLocation=(0,32),
                                  screen=screen,
                                  realXLength=80,
                                  realZLength=80,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="3")

        self.mode4Button = Button(elementId="mode4",
                                  gameBoardLocation=[0, 0, 0],
                                  screenLocation=(32,32),
                                  screen=screen,
                                  realXLength=80,
                                  realZLength=80,
                                  pixelHeight=32,
                                  pixelWidth=32,
                                  textElement="4")

        self.confirmButton = Button(elementId="confirm",
                                    gameBoardLocation=[0, 0, 170],
                                    screenLocation=(65,40),
                                    screen=screen,
                                    realXLength=53.33,
                                    realZLength=70,
                                    pixelHeight=19,
                                    pixelWidth=62,
                                    textElement="Confirm")

        self.currentGameModeText = Text(elementId="currentGameMode",
                                        screenLocation=(65, 0),
                                        screen=self._screen,
                                        fontSize=9)

    def draw(self):
        self.mode1Button.draw()
        self.mode2Button.draw()
        self.mode3Button.draw()
        self.mode4Button.draw()
        self.confirmButton.draw()
        self.currentGameModeText.draw("White Human\nvs\nBlack Robot")
"""
difficulty = 1
while True:
    testScreen = PillowComputerScreen()
    print("Text Message Canvas")
    textMessageCanvas = TextMessageCanvas(screen=testScreen)
    textMessageCanvas.draw("Hello World!Hello World!\nHello World!Hello World!\nHello World!Hello World!")
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    print("Yes No Canvas")
    yesNoCanvas = YesNoCanvas(screen=testScreen)
    yesNoCanvas.draw("Yes no question?")
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    print("Game Entry Canvas")
    gameEntryCanvas = GameEntryCanvas(screen=testScreen)
    gameEntryCanvas.draw()
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    print("Difficulty Select Canvas")
    difficultySelectCanvas = DifficultySelectCanvas(screen=testScreen)
    difficultySelectCanvas.draw(str(difficulty))
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    print("Move Select Canvas")
    moveSelectCanvas = MoveSelectCanvas(screen=testScreen)
    moveSelectCanvas.draw(info="Enter Start")
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    print("Game Mode Canvas")
    gameModeCanvas = GameModeCanvas(screen=testScreen)
    gameModeCanvas.draw()
    difficulty += 1
testScreen.tearDown()
"""

