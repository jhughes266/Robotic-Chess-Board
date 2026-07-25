from cmath import inf


class SearchProgress:

    def __init__(self):
        self.__bestCost = inf
        self.__firstIteration = True

    def updateProgress(self, cost):

        if cost < self.__bestCost:
            self.__bestCost = round(cost, 2)
            print("\rL2 distance until goal: " + str(self), end=" ")

    def __str__(self):
        return str(self.__bestCost)