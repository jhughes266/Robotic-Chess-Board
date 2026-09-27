from abc import ABC, abstractmethod
from managers.game_manager.user_interface.ui_canvas_element import *
import numpy as np
class UiCanvas(ABC):
    pass

class TextMessageCanvas(UiCanvas):
    pass

class YesNoCanvas(UiCanvas):
    pass

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
    pass

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
                
        