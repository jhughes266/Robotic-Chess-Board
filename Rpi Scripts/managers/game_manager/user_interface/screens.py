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
        
        self.__imageWhite = Image.new("1", (self.__screenWidth, self.__screenHeight), (0))
        self.__drawWhite = ImageDraw.Draw(self.__imageWhite)
        
        self.__imageBlack = Image.new("1", (self.__screenWidth, self.__screenHeight), (0))
        self.__drawBlack = ImageDraw.Draw(self.__imageBlack)
    
    def __getDrawList(self, displayScreen):
        drawList = []
        if len(displayScreen) == 2:
            drawList.append(self.__drawWhite)
            drawList.append(self.__drawBlack)
        elif displayScreen[0] == "White":
            drawList.append(self.__drawWhite)
        elif displayScreen[0] == "Black":
            drawList.append(self.__drawBlack)
        
        
        return drawList
    
    def __getImageList(self, displayScreen):
        imageList = []
        if len(displayScreen) == 2:
            imageList.append(self.__imageWhite)
            imageList.append(self.__imageBlack)
        elif displayScreen[0] == "White":
            imageList.append(self.__imageWhite)
        elif displayScreen[0] == "Black":
            imageList.append(self.__imageBlack)
        
        return imageList
    
    def setUp(self):
        pass

    def tearDown(self):
        cv2.destroyAllWindows()

    def pasteImage(self, xy, imageToPaste, displayScreen):
        for image in self.__getImageList(displayScreen=displayScreen):
            image.paste(imageToPaste, xy)

    def drawRectangle(self, xy, displayScreen, fill=None, outline=None, width=1):
        for draw in self.__getDrawList(displayScreen=displayScreen):
            draw.rectangle(xy, fill=fill, outline=outline, width=width)
    
    def drawMouse(self, xy, displayScreen):
        centreX = xy[0]
        centreY = xy[1]
        
        for draw in self.__getDrawList(displayScreen=displayScreen):            
            draw.point((centreX-1, centreY-1), fill=1)
            draw.point((centreX, centreY-1), fill=0)
            draw.point((centreX+1, centreY-1), fill=1)
            draw.point((centreX-1, centreY), fill=0)
            draw.point((centreX, centreY), fill=1)
            draw.point((centreX+1, centreY), fill=0)
            draw.point((centreX-1, centreY+1), fill=1)
            draw.point((centreX, centreY+1), fill=0)
            draw.point((centreX+1, centreY+1), fill=1)

    def drawText(self, xy, text, displayScreen, fill=1, fontSize=None, anchor=None):
        for draw in self.__getDrawList(displayScreen=displayScreen):            
            draw.multiline_text(xy, text, fill=fill, font_size=fontSize, anchor=anchor)

    def display(self, displayScreen):
        scaleFactor = 6
        for screen, image in zip(displayScreen, self.__getImageList(displayScreen=displayScreen)):
            npArray = np.array(image, dtype=np.uint8)*255
            scaledImage = cv2.resize(npArray, (self.__screenWidth*scaleFactor, self.__screenHeight*scaleFactor), interpolation=cv2.INTER_AREA)
            cv2.imshow(screen, scaledImage)
        self.clearDisplay(displayScreen=displayScreen)

    def clearDisplay(self, displayScreen):
        for draw in self.__getDrawList(displayScreen=displayScreen):            
            draw.rectangle((0, 0, self.__screenWidth, self.__screenHeight), outline=0, fill=0)