from config import *
from abc import ABC, abstractmethod
import chess
import numpy as np
from PIL import Image, ImageDraw

if SCREEN_TYPE == "oled":
    from luma.core.interface.serial import i2c
    from luma.core.render import canvas
    from luma.oled.device import ssd1309
elif SCREEN_TYPE == "default":
    import cv2


class Screens(ABC):

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
    def _clearDisplay(self):
        pass

class PillowComputerScreens(Screens):
    def __init__(self):
        self.__screenWidth = 128
        self.__screenHeight = 64

        self.__imageWhite = Image.new("1", (self.__screenWidth, self.__screenHeight), (0))
        self.__drawWhite = ImageDraw.Draw(self.__imageWhite)
        
        self.__imageBlack = Image.new("1", (self.__screenWidth, self.__screenHeight), (0))
        self.__drawBlack = ImageDraw.Draw(self.__imageBlack)
        
        self._chessColourAsString = {
            1:"white",
            0:"black"
            }
    
    def __getDrawList(self, displayScreen):
        drawList = []
        if len(displayScreen) == 2:
            assert displayScreen[0] == chess.WHITE, "When feeding in two display screens the first must be chess.WHITE and the second chess.BLACK!"
            drawList.append(self.__drawWhite)
            drawList.append(self.__drawBlack)
        elif displayScreen[0] == chess.WHITE:
            drawList.append(self.__drawWhite)
        elif displayScreen[0] == chess.BLACK:
            drawList.append(self.__drawBlack)
        else:
            assert True, "THERE IS SOMETHING WRONG WITH THE SCREEN NAMING! IT MUST BE IN LIST FORM AND EITHER chess.WHITE or chess.BLACK or both in seperate elements!"
        
        
        return drawList
    
    def __getImageList(self, displayScreen):
        imageList = []
        if len(displayScreen) == 2:
            assert displayScreen[0] == chess.WHITE, "When feeding in two display screens the first must be chess.WHITE and the second chess.BLACK!"
            imageList.append(self.__imageWhite)
            imageList.append(self.__imageBlack)
        elif displayScreen[0] == chess.WHITE:
            imageList.append(self.__imageWhite)
        elif displayScreen[0] == chess.BLACK:
            imageList.append(self.__imageBlack)
        else:
            assert True, "THERE IS SOMETHING WRONG WITH THE SCREEN NAMING! IT MUST BE IN LIST FORM AND EITHER chess.WHITE or chess.BLACK or both in seperate elements!"
        
        return imageList

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
            cv2.imshow(self._chessColourAsString[screen], scaledImage)
        cv2.waitKey(1)
        self._clearDisplay(displayScreen=displayScreen)

    def _clearDisplay(self, displayScreen):
        for draw in self.__getDrawList(displayScreen=displayScreen):            
            draw.rectangle((0, 0, self.__screenWidth, self.__screenHeight), outline=0, fill=0)

class PillowOledScreens(PillowComputerScreens):
    def __init__(self):
        whiteScreenAddress = 0x3c
        blackScreenAddress = 0x3e

        self.__serialWhite = i2c(port=1, address=whiteScreenAddress)
        self.__serialBlack = i2c(port=1, address=blackScreenAddress)

        self.__deviceWhite = ssd1309(self.__serialWhite)
        self.__deviceBlack = ssd1309(self.__serialBlack)

        self.__screenWidth = 128
        self.__screenHeight = 64

        self.__imageWhite = Image.new("1", (self.__screenWidth, self.__screenHeight), (0))
        self.__drawWhite = ImageDraw.Draw(self.__imageWhite)

        self.__imageBlack = Image.new("1", (self.__screenWidth, self.__screenHeight), (0))
        self.__drawBlack = ImageDraw.Draw(self.__imageBlack)

        self._chessColourAsString = {
            1: "white",
            0: "black"
        }


    def __getDeviceList(self, displayScreen):
        deviceList = []
        if len(displayScreen) == 2:
            assert displayScreen[0] == chess.WHITE, "When feeding in two display screens the first must be chess.WHITE and the second chess.BLACK!"
            deviceList.append(self.__deviceWhite)
            deviceList.append(self.__deviceBlack)
        elif displayScreen[0] == chess.WHITE:
            deviceList.append(self.__deviceWhite)
        elif displayScreen[0] == chess.BLACK:
            deviceList.append(self.__deviceBlack)
        else:
            assert True, "THERE IS SOMETHING WRONG WITH THE SCREEN NAMING! IT MUST BE IN LIST FORM AND EITHER chess.WHITE or chess.BLACK or both in separate elements!"

        return deviceList

    def tearDown(self):
        self.__deviceWhite.clear()
        self.__deviceWhite.cleanup()
        self.__serialWhite.cleanup()

        self.__deviceBlack.clear()
        self.__deviceBlack.cleanup()
        self.__serialBlack.cleanup()

    def display(self, displayScreen):
        for image, device in zip(self.__getImageList(displayScreen=displayScreen), self.__getDeviceList(displayScreen=displayScreen)):
            device.display(image)
        self._clearDisplay(displayScreen=displayScreen)

"""
# Test script for the OLED screens
testScreens = PillowComputerScreens()
testScreens.pasteImage(xy=(10, 20),
                       imageToPaste=Image.open("ui_images/pawn.jpg"),
                       displayScreen=[chess.WHITE, chess.BLACK])



testScreens.drawMouse(xy=(30, 20),
                      displayScreen=[chess.WHITE, chess.BLACK])

testScreens.drawText(xy=(35, 20),
                     text="White screen",
                     displayScreen=[chess.WHITE])

testScreens.drawText(xy=(35, 20),
                     text="Black screen",
                     displayScreen=[chess.BLACK])

testScreens.drawRectangle(xy=(70, 40, 75, 60),
                          displayScreen=[chess.WHITE, chess.BLACK],
                          outline=1)

testScreens.display(displayScreen=[chess.WHITE, chess.BLACK])
input()
testScreens.tearDown()
"""
