from abc import ABC, abstractmethod


class UiCanvasElement(ABC):
    def __init__(self, elementId, gameBoardLocation, screenLocation, screen):
        self.elementId = elementId
        self._gameBoardLocation = gameBoardLocation
        #(x,y)
        self._screenLocation = screenLocation
        self._screen = screen
    
    @abstractmethod
    def draw(self):
        pass
    

class Button(UiCanvasElement):
    __clickHeight = 60
    __clickResetHeight = 70
    def __init__(self, elementId, gameBoardLocation, screenLocation, screen, realXLength, realZLength, pixelHeight, pixelWidth, textElement):
        super().__init__(elementId, gameBoardLocation, screenLocation, screen)
        self.__clicked = False
        self.__realXLength = realXLength
        self.__realZLength = realZLength
        self.__pixelHeight = pixelHeight
        self.__pixelWidth = pixelWidth
        self.__textElement = textElement
    
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
        return (stylusX > gameBoardLocationX) and (stylusZ > gameBoardLocationZ) and (stylusX < (gameBoardLocationX + self.__realXLength)) and((stylusZ < (gameBoardLocationZ + self.__realZLength)))

    def draw(self):
        x0 = self._screenLocation[0]
        y0 = self._screenLocation[1]
        # Minus one takes into account that the x0 square is included
        x1 = x0 + self.__pixelWidth - 1
        y1 = y0 + self.__pixelHeight - 1
        if not self.__clicked:
            self._screen.drawRectangle((x0, y0, x1, y1), fill=None, outline=None, width=1)
            self._screen.drawText((x0 + 1, y0 + 1), text=self.__textElement, fill=1)
        else:
            self._screen.drawRectangle((x0, y0, x1, y1), fill=1, outline=None, width=1)
            self._screen.drawText((x0 + 1, y0 + 1), text=self.__textElement, fill=0)

class Text(UiCanvasElement):
    def __init__(self, elementId, screenLocation, screen):
        super().__init__(elementId=elementId,
                         gameBoardLocation=None,
                         screenLocation=screenLocation,
                         screen=screen)

    def draw(self, text):
        self._screen.drawText(xy=self._screenLocation, text=text)

class Image(UiCanvasElement):
    def __init__(self, screenLocation, screen):
        super().__init__(screenLocation, screen, gameBoardLocation=None)

    def draw(self, bitmap):
        self._screen.drawBitmap(xy=self._screenLocation, bitmap=bitmap)