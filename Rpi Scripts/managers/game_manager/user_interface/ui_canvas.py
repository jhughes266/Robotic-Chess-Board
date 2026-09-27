from abc import ABC, abstractmethod
from managers.game_manager.user_interface.ui_canvas_element import *
import numpy as np
class UiCanvas(ABC):
    pass

class TextMessageCanvas(UiCanvas):
    pass

class YesNoCanvas(UiCanvas):
    def __init__(self):
        self.yesButton = Button(elementId="yesButton",
                                 gameBoardLocation=[0, 0, 0],
                                 screenLocation=None,
                                 screen=None,
                                 realXLength=80,
                                 realZLength=160,
                                 pixelHeight=None,
                                 pixelWidth=None)

        self.noButton = Button(elementId="noButton",
                                  gameBoardLocation=[80, 0, 0],
                                  screenLocation=None,
                                  screen=None,
                                  realXLength=80,
                                  realZLength=160,
                                  pixelHeight=None,
                                  pixelWidth=None)

class GameEntryCanvas(UiCanvas):
    def __init__(self):
        self.quitButton = Button(elementId="quitButton",
                             gameBoardLocation=[0,0,0],
                             screenLocation=None,
                             screen=None,
                             realXLength=80,
                             realZLength=240,
                             pixelHeight=None,
                             pixelWidth=None)
        
        self.startButton = Button(elementId="startButton",
                             gameBoardLocation=[80,0,0],
                             screenLocation=None,
                             screen=None,
                             realXLength=80,
                             realZLength=240,
                             pixelHeight=None,
                             pixelWidth=None)    

class DifficultySelectCanvas(UiCanvas):
    def __init__(self):
        self.difficulty1Button = Button(elementId="difficulty1",
                                 gameBoardLocation=[106.66, 0, 0],
                                 screenLocation=None,
                                 screen=None,
                                 realXLength=53.33,
                                 realZLength=53.33,
                                 pixelHeight=None,
                                 pixelWidth=None)

        self.difficulty2Button = Button(elementId="difficulty2",
                                  gameBoardLocation=[106.66, 0, 53.33],
                                  screenLocation=None,
                                  screen=None,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=None,
                                  pixelWidth=None)

        self.difficulty3Button = Button(elementId="difficulty3",
                                  gameBoardLocation=[53.33, 0, 0],
                                  screenLocation=None,
                                  screen=None,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=None,
                                  pixelWidth=None)

        self.difficulty4Button = Button(elementId="difficulty4",
                                  gameBoardLocation=[53.33, 0, 53.33],
                                  screenLocation=None,
                                  screen=None,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=None,
                                  pixelWidth=None)

        self.difficulty5Button = Button(elementId="difficulty5",
                                  gameBoardLocation=[0, 0, 0],
                                  screenLocation=None,
                                  screen=None,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=None,
                                  pixelWidth=None)

        self.difficulty6Button = Button(elementId="difficulty6",
                                  gameBoardLocation=[0, 0, 53.33],
                                  screenLocation=None,
                                  screen=None,
                                  realXLength=53.33,
                                  realZLength=53.33,
                                  pixelHeight=None,
                                  pixelWidth=None)

        self.confirmButton = Button(elementId="confirm",
                                  gameBoardLocation=[0, 0, 120],
                                  screenLocation=None,
                                  screen=None,
                                  realXLength=53.33,
                                  realZLength=120,
                                  pixelHeight=None,
                                  pixelWidth=None)

class MoveSelectCanvas(UiCanvas):
    def __init__(self):
        self.__chessBoardButtonArray = self.__constructChessBoardButtonArray()
        self.confirmButton = Button(elementId="confirmButton",
                             gameBoardLocation=[120,0,180],
                             screenLocation=None,
                             screen=None,
                             realXLength=40,
                             realZLength=70,
                             pixelHeight=None,
                             pixelWidth=None)
        
        self.resetButton = Button(elementId="resetButton",
                             gameBoardLocation=[0,0,180],
                             screenLocation=None,
                             screen=None,
                             realXLength=40,
                             realZLength=70,
                             pixelHeight=None,
                             pixelWidth=None)
        
    def __constructChessBoardButtonArray(self):
        chessBoardButtonArray = []
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
        realSideLength = 20
        
        for zIdx, file in enumerate(files):
            for xIdx, rank in enumerate(ranks):
                button = Button(elementId=file+rank,
                             gameBoardLocation=[0+xIdx*realSideLength, 0, 0+zIdx*realSideLength],
                             screenLocation=None,
                             screen=None,
                             realXLength=realSideLength,
                             realZLength=realSideLength,
                             pixelHeight=None,
                             pixelWidth=None)
                chessBoardButtonArray.append(button)
        return chessBoardButtonArray
                
    def findClickedSquare(self, stylusGameBoardLocation):
        for button in self.__chessBoardButtonArray:
            if button.isClicked(stylusGameBoardLocation):
                return button.elementId
        return None

class GameModeCanvas(UiCanvas):
    def __init__(self):
        self.mode1Button = Button(elementId="mode1",
                                 gameBoardLocation=[80, 0, 0],
                                 screenLocation=None,
                                 screen=None,
                                 realXLength=80,
                                 realZLength=80,
                                 pixelHeight=None,
                                 pixelWidth=None)

        self.mode2Button = Button(elementId="mode2",
                            gameBoardLocation=[80, 0, 80],
                            screenLocation=None,
                            screen=None,
                            realXLength=80,
                            realZLength=80,
                            pixelHeight=None,
                            pixelWidth=None)

        self.mode3Button = Button(elementId="mode3",
                            gameBoardLocation=[0, 0, 0],
                            screenLocation=None,
                            screen=None,
                            realXLength=80,
                            realZLength=80,
                            pixelHeight=None,
                            pixelWidth=None)

        self.mode4Button = Button(elementId="mode4",
                            gameBoardLocation=[0, 0, 0],
                            screenLocation=None,
                            screen=None,
                            realXLength=80,
                            realZLength=80,
                            pixelHeight=None,
                            pixelWidth=None)

        self.confirmButton = Button(elementId="confirm",
                                    gameBoardLocation=[0, 0, 170],
                                    screenLocation=None,
                                    screen=None,
                                    realXLength=53.33,
                                    realZLength=70,
                                    pixelHeight=None,
                                    pixelWidth=None)


        