from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont
import os
import time

class Screen(ABC):
    @abstractmethod
    def setUp(self):
        pass

    @abstractmethod
    def tearDown(self):
        pass

    @abstractmethod
    def drawBitmap(self, xy, bitmap):
        pass

    @abstractmethod
    def drawRectangle(self, xy, fill=None, outline=None, width=1):
        pass

    @abstractmethod
    def drawText(self,  xy, text, fill=1):
        pass

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def clearDisplay(self):
        pass

class PillowComputerScreen(Screen):
    def __init__(self):
        self.__screenWidth = 128
        self.__screenHeight = 64
        self.__image = Image.new("1", (self.__screenWidth, self.__screenHeight), (0))
        self.__draw = ImageDraw.Draw(self.__image)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def drawBitmap(self, xy, bitmap):
        pass

    def drawRectangle(self, xy, fill=None, outline=None, width=1):
        self.__draw.rectangle(xy, fill=fill, outline=outline, width=width)

    def drawText(self, xy, text, fill=1, fontSize=None, anchor=None):
        self.__draw.multiline_text(xy, text, fill=fill, font_size=fontSize, anchor=anchor)

    def display(self):
        self.__image.show()
        self.clearDisplay()

    def clearDisplay(self):
        self.__draw.rectangle((0, 0, self.__screenWidth, self.__screenHeight), outline=0, fill=0)