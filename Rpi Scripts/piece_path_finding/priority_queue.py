
class PriorityQueue:
    """
    A priority queue that allows its internal collection to be sorted by a lamda
    """
    def __init__(self, sortingLambda=lambda x: x):
        """
        Constructor for the priority queue.
        Args:
            sortingLambda: A lambda that is used to sort the elements in the queue.
        """
        self.__elements = []
        self.__sortingLambda = sortingLambda

    def __len__(self):
        """
        Returns the number of elements in the queue.
        Returns:
            The number of elements in the queue.
        """
        return len(self.__elements)

    def empty(self):
        """
        Returns whether the queue is empty.
        Returns:
            True if the queue is empty, otherwise False.
        """
        return len(self) == 0

    def push(self, item):
        """
        Adds an element to the queue and sorts it according to the lambda.
        Args:
            item: The element to add to the queue.
        """
        self.__elements.append(item)
        self.__elements.sort(key=self.__sortingLambda)

    def pop(self):
        """
        Removes and returns the next element from the queue.
        Returns:
             The first element in the queue.
        """
        return self.__elements.pop(0)

    def top(self):
        """
        Returns but DOES NOT remove the element that is first in the queue.
        Returns:
             First element in the queue.
        """
        return self.__elements[0]

