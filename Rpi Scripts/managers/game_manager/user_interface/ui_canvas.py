from abc import ABC, abstractmethod

from managers.game_manager.user_interface.screen import ConsoleScreen
from managers.game_manager.user_interface.ui_canvas_element import *
import numpy as np


class UiCanvas(ABC):
    def __init__(self, screen):
        self._screen = screen

    @abstractmethod
    def draw(self):
        pass

class TextMessageCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.text = Text(elementId="yesNoSelection", screenLocation=(10, 20), screen=self._screen)

    def draw(self, text):
        self.text.draw(text)
        self._screen.display()

class YesNoCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.yesButton = Button(elementId="yesButton",
                                 gameBoardLocation=[0, 0, 0],
                                 screenLocation=(0, 14),
                                 screen=screen,
                                 realXLength=80,
                                 realZLength=160,
                                 pixelHeight=25,
                                 pixelWidth=128,
                                 textElement="YES")

        self.noButton = Button(elementId="noButton",
                                  gameBoardLocation=[80, 0, 0],
                                  screenLocation=(0, 39),
                                  screen=screen,
                                  realXLength=80,
                                  realZLength=160,
                                  pixelHeight=25,
                                  pixelWidth=128,
                                  textElement="NO")

        self.text = Text(elementId="yesNoSelection", screenLocation=(0, 0), screen=self._screen)

    def draw(self, yesNoQuestion):
        self.yesButton.draw()
        self.noButton.draw()
        self.text.draw(text=yesNoQuestion)
        self._screen.display()

class GameEntryCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.quitButton = Button(elementId="quitButton",
                             gameBoardLocation=[0,0,0],
                             screenLocation=(0,0),
                             screen=screen,
                             realXLength=80,
                             realZLength=240,
                             pixelHeight=32,
                             pixelWidth=124,
                             textElement="QUIT")
        
        self.startButton = Button(elementId="startButton",
                             gameBoardLocation=[80,0,0],
                             screenLocation=(0,31),
                             screen=screen,
                             realXLength=80,
                             realZLength=240,
                             pixelHeight=32,
                             pixelWidth=124,
                             textElement="START")

    def draw(self):
        self.quitButton.draw()
        self.startButton.draw()
        self._screen.display()

class DifficultySelectCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.difficulty1Button = Button(elementId="difficulty1",
                                 gameBoardLocation=[106.66, 0, 0],
                                 screenLocation=(0,0),
                                 screen=screen,
                                 realXLength=53.33,
                                 realZLength=53.33,
                                 pixelHeight=21,
                                 pixelWidth=21,
                                 textElement="Very Easy")

        self.difficulty2Button = Button(elementId="difficulty2",
                                  gameBoardLocation=[106.66, 0, 53.33],
                                  screenLocation=(21,0),
                                  screen=screen,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=21,
                                  pixelWidth=21,
                                  textElement="Easy")

        self.difficulty3Button = Button(elementId="difficulty3",
                                  gameBoardLocation=[53.33, 0, 0],
                                  screenLocation=(0,21),
                                  screen=screen,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=21,
                                  pixelWidth=21,
                                  textElement="Medium")

        self.difficulty4Button = Button(elementId="difficulty4",
                                  gameBoardLocation=[53.33, 0, 53.33],
                                  screenLocation=(21,21),
                                  screen=screen,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=21,
                                  pixelWidth=21,
                                  textElement="Hard")

        self.difficulty5Button = Button(elementId="difficulty5",
                                  gameBoardLocation=[0, 0, 0],
                                  screenLocation=(0,42),
                                  screen=screen,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=21,
                                  pixelWidth=21,
                                  textElement="Very Hard")

        self.difficulty6Button = Button(elementId="difficulty6",
                                  gameBoardLocation=[0, 0, 53.33],
                                  screenLocation=(21,42),
                                  screen=screen,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=21,
                                  pixelWidth=21,
                                  textElement="Extreme")

        self.confirmButton = Button(elementId="confirm",
                                  gameBoardLocation=[0, 0, 120],
                                  screenLocation=(64,45),
                                  screen=screen,
                                  realXLength=53.33,
                                  realZLength=120,
                                  pixelHeight=18,
                                  pixelWidth=64,
                                  textElement="CONFIRM")

        self.text = Text(elementId="yesNoSelection", screenLocation=(64, 0), screen=self._screen)

        self.__buttonList = [self.difficulty1Button, self.difficulty2Button, self.difficulty3Button, self.difficulty4Button, self.difficulty5Button, self.difficulty6Button, self.confirmButton]

    def draw(self, difficulty):
        for button in self.__buttonList:
            button.draw()
        self.text.draw(difficulty)
        self._screen.display()

class MoveSelectCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.__chessBoardButtonArray = self.__constructChessBoardButtonArray()
        self.confirmButton = Button(elementId="confirmButton",
                             gameBoardLocation=[120,0,180],
                             screenLocation=None,
                             screen=screen,
                             realXLength=40,
                             realZLength=70,
                             pixelHeight=None,
                             pixelWidth=None,
                             textElement=None)
        
        self.resetButton = Button(elementId="resetButton",
                             gameBoardLocation=[0,0,180],
                             screenLocation=None,
                             screen=screen,
                             realXLength=40,
                             realZLength=70,
                             pixelHeight=None,
                             pixelWidth=None,
                             textElement=None)
        
    def __constructChessBoardButtonArray(self):
        chessBoardButtonArray = []
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
        realSideLength = 20
        pixelSideLength = 6
        
        for zIdx, file in enumerate(files):
            for xIdx, rank in enumerate(ranks):
                button = Button(elementId=file+rank,
                             gameBoardLocation=[0+xIdx*realSideLength, 0, 0+zIdx*realSideLength],
                             screenLocation=None,
                             screen=self._screen,
                             realXLength=realSideLength,
                             realZLength=realSideLength,
                             pixelHeight=None,
                             pixelWidth=None,
                             textElement=None)
                chessBoardButtonArray.append(button)
        return chessBoardButtonArray
                
    def findClickedSquare(self, stylusGameBoardLocation):
        for button in self.__chessBoardButtonArray:
            if button.isClicked(stylusGameBoardLocation):
                return button.elementId
        return None

    def draw(self):
        pass

class GameModeCanvas(UiCanvas):
    def __init__(self, screen):
        super().__init__(screen)
        self.mode1Button = Button(elementId="mode1",
                                 gameBoardLocation=[80, 0, 0],
                                 screenLocation=None,
                                 screen=screen,
                                 realXLength=80,
                                 realZLength=80,
                                 pixelHeight=None,
                                 pixelWidth=None,
                                 textElement=None)

        self.mode2Button = Button(elementId="mode2",
                            gameBoardLocation=[80, 0, 80],
                            screenLocation=None,
                            screen=screen,
                            realXLength=80,
                            realZLength=80,
                            pixelHeight=None,
                            pixelWidth=None,
                            textElement=None)

        self.mode3Button = Button(elementId="mode3",
                            gameBoardLocation=[0, 0, 0],
                            screenLocation=None,
                            screen=screen,
                            realXLength=80,
                            realZLength=80,
                            pixelHeight=None,
                            pixelWidth=None,
                            textElement=None)

        self.mode4Button = Button(elementId="mode4",
                            gameBoardLocation=[0, 0, 0],
                            screenLocation=None,
                            screen=screen,
                            realXLength=80,
                            realZLength=80,
                            pixelHeight=None,
                            pixelWidth=None,
                            textElement=None)

        self.confirmButton = Button(elementId="confirm",
                                    gameBoardLocation=[0, 0, 170],
                                    screenLocation=None,
                                    screen=screen,
                                    realXLength=53.33,
                                    realZLength=70,
                                    pixelHeight=None,
                                    pixelWidth=None,
                                    textElement=None)
    def draw(self):
        pass

testScreen = ConsoleScreen()
testCanvas = DifficultySelectCanvas(screen=testScreen)
testCanvas.draw("5")