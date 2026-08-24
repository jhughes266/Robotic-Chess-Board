from cmath import inf


class SearchProgress:
    """
    This class is not essential but is used to track the progress of the search and determine the progress of the search.
    """
    def __init__(self):
        """
        Constructor for the SearchProgress class.
        """
        # The best recorded cost so far
        self.__bestCost = inf
        # First iteration flag
        self.__firstIteration = True

    def updateProgress(self, cost):
        """
        Updates the progress of the search. If a better cost has been found it stores it and then prints it.
        Args:
            cost: incoming cost
        """
        if cost < self.__bestCost:
            self.__bestCost = round(cost, 2)
            print("\rL2 distance until goal: " + str(self), end=" ")

    def __str__(self):
        """
        Returns the string representation of the search progress.
        Returns:
             A string that is the best cost.
        """
        return str(self.__bestCost)