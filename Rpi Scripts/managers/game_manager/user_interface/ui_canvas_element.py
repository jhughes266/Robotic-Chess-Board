from abc import ABC, abstractmethod

from sympy.physics.units import current


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
    def __init__(self, elementId, gameBoardLocation, screenLocation, screen, realXLength, realZLength, pixelHeight, pixelWidth, textElement, fontSize=None, fill=0):
        super().__init__(elementId, gameBoardLocation, screenLocation, screen)
        self.__clicked = False
        self.__realXLength = realXLength
        self.__realZLength = realZLength
        self.__pixelHeight = pixelHeight
        self.__pixelWidth = pixelWidth
        self.__textElement = textElement
        self.__fontSize = fontSize
        self.__fill = fill
        self.__clickedFill = fill
    
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

        # Alternate the button fill each draw cycle to make it flash when it is clicked
        currentFill = None
        if not self.__clicked:
            self.__clickedFill = int(not(self.__fill))
            currentFill = self.__fill
        else:
            self.__clickedFill = int(not(self.__clickedFill))
            currentFill = self.__clickedFill

        self._screen.drawRectangle(xy=(x0, y0, x1, y1),
                                   fill=currentFill,
                                   outline=1,
                                   width=1)

        self._screen.drawText(xy=(int((x0 + x1) / 2), int((y0 + y1) / 2)),
                              text=self.__textElement,
                              fill=int(not(currentFill)),
                              fontSize=self.__fontSize,
                              anchor="mm")

class Text(UiCanvasElement):
    def __init__(self, elementId, screenLocation, screen, fontSize=None, anchor=None):
        super().__init__(elementId=elementId,
                         gameBoardLocation=None,
                         screenLocation=screenLocation,
                         screen=screen)
        self.__fontSize = fontSize
        self.__anchor = anchor

    def draw(self, text=None):
        if text is None:
            text = self.elementId
        self._screen.drawText(xy=self._screenLocation,
                              text=text,
                              fontSize=self.__fontSize,
                              anchor=self.__anchor)

class PastedImage(UiCanvasElement):
    def __init__(self, elementId, screenLocation, screen):
        super().__init__(elementId=elementId,
                         gameBoardLocation=None,
                         screenLocation=screenLocation,
                         screen=screen)

    def draw(self, imageToPaste):
        self._screen.pasteImage(xy=self._screenLocation,
                                imageToPaste=imageToPaste)