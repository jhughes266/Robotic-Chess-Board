from abc import ABC, abstractmethod
import os
class UserInterface(ABC):
    def __init__(self, boardManager):
        self._boardManager = boardManager
        self._chessColourAsText = ['Black', 'White']

    @abstractmethod
    def playerSelectMove(self):
        pass

    @abstractmethod
    def displayText(self, str):
        pass

    @abstractmethod
    def yesOrNoQuestion(self, str):
        pass

    @abstractmethod
    def selectDifficulty(self):
        pass



class TextUserInterface(UserInterface):
    def playerSelectMove(self):
        return input("Please enter your move!: ")

    def displayText(self, str):
        print(str)

    def yesOrNoQuestion(self, str):
        str += "\nEnter NO or YES:\nSelection: "
        return input(str)

    def selectDifficulty(self):
        return input(f"Please select a difficulty from the following list:\n1: Very Easy (2 ply depth)\n2: Easy(3 ply depth)\n3: Medium (4 ply depth)\n4: Hard (5 ply depth)\n5: Very Hard (6 ply depth)\n6: Extreme (Will search to whatever depth it can within maximum search time!)\n(Please note that irrespective of the difficulty the game will search for at most the maximum search time.)\nSelection: ")

class HandUserInterface(UserInterface):
    def playerSelectMove(self):
        pass

    def displayText(self, str):
        pass

    def yesOrNoQuestion(self, str):
        pass

    def selectDifficulty(self):
        pass
