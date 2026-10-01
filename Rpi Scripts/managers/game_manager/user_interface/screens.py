from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont
import os
import time
import cv2
import numpy as np

class Screens(ABC):
    @abstractmethod
    def setUp(self):
        pass

    @abstractmethod
    def tearDown(self):
        pass

    @abstractmethod
    def pasteImage(self, xy, imageToPaste):
        pass

    @abstractmethod
    def drawRectangle(self, xy, fill=None, outline=None, width=1):
        pass
    
    @abstractmethod
    def drawMouse(self, xy):
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

class PillowComputerScreens(Screens):
    def __init__(self):
        self.__screenWidth = 128
        self.__screenHeight = 64
        self.__image = Image.new("1", (self.__screenWidth, self.__screenHeight), (0))
        self.__draw = ImageDraw.Draw(self.__image)

    def setUp(self):
        pass

    def tearDown(self):
        cv2.destroyAllWindows()

    def pasteImage(self, xy, imageToPaste):
        self.__image.paste(imageToPaste, xy)

    def drawRectangle(self, xy, fill=None, outline=None, width=1):
        self.__draw.rectangle(xy, fill=fill, outline=outline, width=width)
    
    def drawMouse(self, xy):
        centreX = xy[0]
        centreY = xy[1]
        self.__draw.point((centreX-1, centreY-1), fill=1)
        self.__draw.point((centreX, centreY-1), fill=0)
        self.__draw.point((centreX+1, centreY-1), fill=1)
        self.__draw.point((centreX-1, centreY), fill=0)
        self.__draw.point((centreX, centreY), fill=1)
        self.__draw.point((centreX+1, centreY), fill=0)
        self.__draw.point((centreX-1, centreY+1), fill=1)
        self.__draw.point((centreX, centreY+1), fill=0)
        self.__draw.point((centreX+1, centreY+1), fill=1)

    def drawText(self, xy, text, fill=1, fontSize=None, anchor=None):
        self.__draw.multiline_text(xy, text, fill=fill, font_size=fontSize, anchor=anchor)

    def display(self):
        npArray = np.array(self.__image, dtype=np.uint8)*255
        scaleFactor = 6
        scaledImage = cv2.resize(npArray, (self.__screenWidth*scaleFactor, self.__screenHeight*scaleFactor), interpolation=cv2.INTER_AREA)
        cv2.imshow("screen", scaledImage)
        self.clearDisplay()

    def clearDisplay(self):
        self.__draw.rectangle((0, 0, self.__screenWidth, self.__screenHeight), outline=0, fill=0)