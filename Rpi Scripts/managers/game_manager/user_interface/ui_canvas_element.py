from abc import ABC, abstractmethod



class UiCanvasElement(ABC):
    def __init__(self, elementId, screenLocation, screens):
        self.elementId = elementId
        self._gameBoardLocation = None
        #(x,y)
        self._screenLocation = screenLocation
        self._screens = screens
        self._pixPerMm = 0.35625
        # The +63 is the height of the screen (would be 64 but have to -1 because of zero based indexing)
        self._screenHeightPix = 63
    
    @abstractmethod
    def draw(self):
        pass
    
    def _gameBoardLocationToScreen(self, gameBoardLocation):
        xReal, yReal, zReal = gameBoardLocation[0], gameBoardLocation[1], gameBoardLocation[2]
        xScreen = zReal * self._pixPerMm
        yScreen = -xReal * self._pixPerMm + (self._screenHeightPix)
        return xScreen, yScreen
    
    def _screenToGameBoardLocation(self, screenLocation):
        xScreen, yScreen = screenLocation[0], screenLocation[1]
        zReal = xScreen/self._pixPerMm
        xReal =  (self._screenHeightPix - yScreen) / self._pixPerMm
        return (xReal, 0, zReal)
    
    def _pixelLengthToRealLength(self, pixelLength):
        return pixelLength * (1/self._pixPerMm)

class Mouse(UiCanvasElement):
    def __init__(self, elementId, screens):
        super().__init__(elementId, screenLocation=None, screens=screens)
    
    def draw(self, stylusGameBoardLocation):
        xScreen, yScreen = self._gameBoardLocationToScreen(stylusGameBoardLocation)
        self._screens.drawMouse((xScreen, yScreen))
        
        
class Button(UiCanvasElement):
    __clickHeight = 60
    __clickResetHeight = 70
    def __init__(self, elementId, screens, screenLocation, pixelHeight, pixelWidth, textElement, fontSize=None, fill=0):
        super().__init__(elementId, screenLocation, screens)
        self.__clicked = False
        self.__realXLength = self._pixelLengthToRealLength(pixelHeight)
        self.__realZLength = self._pixelLengthToRealLength(pixelWidth)
        self.__pixelHeight = pixelHeight
        self.__pixelWidth = pixelWidth
        self.__textElement = textElement
        self.__fontSize = fontSize
        self.__fill = fill
        self.__clickedFill = fill
        self._gameBoardLocation = self._screenToGameBoardLocation(screenLocation)
    
    def isClicked(self, stylusGameBoardLocation):
        if stylusGameBoardLocation is None:
            self.__clicked = False
            return self.__clicked
        stylusHeight = stylusGameBoardLocation[1]
        stylusX = stylusGameBoardLocation[0]
        stylusZ = stylusGameBoardLocation[2]
        if not self.__stylusInBounds(stylusX, stylusZ):
            self.__clicked = False
        elif stylusHeight < Button.__clickHeight:
            self.__clicked = True
        elif stylusHeight > Button.__clickResetHeight:
            self.__clicked = False
        return self.__clicked
            
    def __stylusInBounds(self, stylusX, stylusZ):
        gameBoardLocationX = self._gameBoardLocation[0]
        gameBoardLocationZ = self._gameBoardLocation[2]
        return (stylusX < gameBoardLocationX) and (stylusZ > gameBoardLocationZ) and (stylusX > (gameBoardLocationX - self.__realXLength)) and((stylusZ < (gameBoardLocationZ + self.__realZLength)))

    def draw(self, textOveride=None):
        x0 = self._screenLocation[0]
        y0 = self._screenLocation[1]
        # Minus one takes into account that the x0 square is included
        x1 = x0 + self.__pixelWidth - 1
        y1 = y0 + self.__pixelHeight - 1

        # Alternate the button fill each draw cycle to make it flash when it is clicked
        currentFill = None
        if not self.__clicked:
            self.__clickedFill = int(not(self.__fill))
            currentFill = self.__fill
        else:
            self.__clickedFill = int(not(self.__clickedFill))
            currentFill = self.__clickedFill

        self._screens.drawRectangle(xy=(x0, y0, x1, y1),
                                   fill=currentFill,
                                   outline=1,
                                   width=1)
        buttonText = None
        if textOveride is not None:
            buttonText = textOveride
        else:
            buttonText = self.__textElement

        self._screens.drawText(xy=(int((x0 + x1) / 2), int((y0 + y1) / 2)),
                              text=buttonText,
                              fill=int(not(currentFill)),
                              fontSize=self.__fontSize,
                              anchor="mm")

class Text(UiCanvasElement):
    def __init__(self, elementId, screenLocation, screens, fontSize=None, anchor=None):
        super().__init__(elementId=elementId,
                         screens=screens,
                         screenLocation=screenLocation,
                        )
        self.__fontSize = fontSize
        self.__anchor = anchor

    def draw(self, text=None):
        if text is None:
            text = self.elementId
        self._screens.drawText(xy=self._screenLocation,
                              text=text,
                              fontSize=self.__fontSize,
                              anchor=self.__anchor)
        
class FlashingRectangle(UiCanvasElement):
    def __init__(self, elementId, screens, screenLocation, pixelHeight, pixelWidth):
        super().__init__(elementId=elementId,
                         screens=screens,
                         screenLocation=screenLocation,
                         )
        
        self.__pixelHeight = pixelHeight
        self.__pixelWidth = pixelWidth
        self.__switchedOn = False
    
    def draw(self):
        x0 = self._screenLocation[0]
        y0 = self._screenLocation[1]
        # Minus one takes into account that the x0 square is included
        x1 = x0 + self.__pixelWidth - 1
        y1 = y0 + self.__pixelHeight - 1
        
        self._screens.drawRectangle(xy=(x0, y0, x1, y1),
                                   fill=0,
                                   outline=self.__switchedOn,
                                   width=1)
        
        self.__switchedOn = not(self.__switchedOn)
        


class PastedImage(UiCanvasElement):
    def __init__(self, elementId, screenLocation, screens):
        super().__init__(elementId=elementId,
                         screenLocation=screenLocation,
                         screens=screens)

    def draw(self, imageToPaste):
        self._screens.pasteImage(xy=self._screenLocation,
                                imageToPaste=imageToPaste)