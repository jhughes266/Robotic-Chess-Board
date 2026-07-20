
class PriorityQueue:

    def __init__(self, sortingLambda=lambda x: x):
        self.__elements = []
        self.__sortingLambda = sortingLambda

    def __len__(self):
        return len(self.__elements)

    def empty(self):
        return len(self) == 0

    def push(self, item):
        self.__elements.append(item)
        self.__elements.sort(key=self.__sortingLambda)

    def pop(self):
        return self.__elements.pop(0)

    def top(self):
        return self.__elements[0]

