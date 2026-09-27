from abc import ABC, abstractmethod
class UiCanvasElement(ABC):
    def __init__(self, elementId, gameBoardLocation, screenLocation, screen):
        self.elementId = elementId
        self._gameBoardLocation = gameBoardLocation
        self._screenLocation = screenLocation
        self._screen = screen
    
    @abstractmethod
    def drawOnScreen(self):
        pass
    

class Button(UiCanvasElement):
    __clickHeight = 60
    __clickResetHeight = 70
    def __init__(self, elementId, gameBoardLocation, screenLocation, screen, realXLength, realZLength, pixelHeight, pixelWidth):
        super().__init__(elementId, gameBoardLocation, screenLocation, screen)
        self.__clicked = False
        self.__realXLength = realXLength
        self.__realZLength = realZLength
    
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
    
    def drawOnScreen(self):
        pass

class Text(UiCanvasElement):
    def __init__(self, gameBoardLocation, screenLocation, screen):
        super().__init__(gameBoardLocation, screenLocation, screen)

class Image(UiCanvasElement):
    def __init__(self, gameBoardLocation, screenLocation, screen):
        super().__init__(gameBoardLocation, screenLocation, screen)