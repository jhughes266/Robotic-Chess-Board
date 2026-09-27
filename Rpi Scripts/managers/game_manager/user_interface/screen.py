from abc import ABC, abstractmethod
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
    def drawBitmap(self):
        pass

    @abstractmethod
    def drawRectangle(self):
        pass

    @abstractmethod
    def drawText(self):
        pass

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def clearDisplay(self):
        pass

class ConsoleScreen(Screen):
    def __init__(self):
        self.__screenArray = []
        self.__screenWidth = 128
        self.__screenHeight = 64
        for i in range(self.__screenHeight):
            self.__screenArray.append([0]*self.__screenWidth)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def drawBitmap(self, xy, bitmap):
        x0 = xy[0]
        y0 = xy[1]

        for y, row in enumerate(bitmap):
            for x, value in enumerate(row):
                self.__screenArray[y0 + y][x0 + x] = value

    def drawRectangle(self, xy, fill=None, outline=None, width=1):
        x0 = xy[0]
        y0 = xy[1]
        x1 = xy[2]
        y1 = xy[3]
        if fill is not None:
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    self.__screenArray[y][x] = 1
            return

        # Top
        for yOffset in range(width):
            for x in range(x0, x1 + 1):
                self.__screenArray[y0 + yOffset][x] = 1

        # Left
        for xOffset in range(width):
            for y in range(y0, y1 + 1):
                self.__screenArray[y][x0 + xOffset] = 1

        # Bottom
        for yOffset in range(width):
            for x in range(x0, x1 + 1):
                self.__screenArray[y1 - yOffset][x] = 1

        # Left
        for xOffset in range(width):
            for y in range(y0, y1 + 1):
                self.__screenArray[y][x1 - xOffset] = 1

    def drawText(self, xy, text, fill=1):
        x0 = xy[0]
        y0 = xy[1]
        for x, char in enumerate(text):
            self.__screenArray[y0][x0+x] = char

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("#" * (self.__screenWidth+2), end="\n#")
        for i, yPixel in enumerate(range(len(self.__screenArray))):
            for xPixel in range(len(self.__screenArray[0])):
                if self.__screenArray[yPixel][xPixel] == 0:
                    print(" ", end="")
                elif self.__screenArray[yPixel][xPixel] == 1:
                    print("\u2588", end="")
                else:
                    print(self.__screenArray[yPixel][xPixel], end="")
            print(f"#\n#",end="")
        print("#" * (self.__screenWidth + 1), end="\n")

        self.clearDisplay()

    def clearDisplay(self):
        for y in range(len(self.__screenArray)):
            for x in range(len(self.__screenArray[0])):
                self.__screenArray[y][x] = 0


"""
testConsoleScreen = ConsoleScreen()
bitmap = [
    [1,0],
    [0,1],
    [1,0]
]
testConsoleScreen.drawBitmap(xy=(50, 10), bitmap=bitmap)
testConsoleScreen.drawText(xy=(10, 40), text="Hello")
testConsoleScreen.drawRectangle(xy=(90, 30, 100, 50), fill=None, outline=None, width=1)
testConsoleScreen.display()

"""

