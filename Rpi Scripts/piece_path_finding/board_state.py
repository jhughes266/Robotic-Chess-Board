from pip._internal.models import candidate
import copy

from piece_path_finding.action import Action
from piece_path_finding.piece_path_finding_config import boardStartStateDictionary


class BoardState:

    def __init__(self, boardStateDictionary):
        self.__boardStateDictionary = boardStateDictionary

        self.__adjacentSquareHelper = [
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1]
        ]
        self.__maxCoordinate = 11
        self.__minCoordinate = 0

        self.__boardPositionMatrix = self.__generateBoardPositionMatrix()

    def __generateBoardPositionMatrix(self):
        boardPositionMatrix = []
        for i in range(self.__maxCoordinate + 1):
            boardPositionMatrix.append([None] * (self.__maxCoordinate + 1))

        for key in self.__boardStateDictionary.keys():
            x = self.__boardStateDictionary[key][0]
            y = self.__boardStateDictionary[key][1]
            boardPositionMatrix[x][y] = key

        return boardPositionMatrix

    def __actionOutsideBoard(self, action):
        if action.destination[0] > self.__maxCoordinate or action.destination[1] > self.__maxCoordinate or action.destination[
            0] < self.__minCoordinate or action.destination[1] < self.__minCoordinate:
            return True

        return False

    def __actionCausesPieceCollision(self, action):
        x = action.destination[0]
        y = action.destination[1]
        if self.__boardPositionMatrix[x][y] is not None:
            return True

        return False

    def actions(self):
        actionList = []
        i = 0
        for key in self.__boardStateDictionary.keys():
            for coordinate in self.__adjacentSquareHelper:

                candidateAction = Action(piece=key, initialPosition = [
                    self.__boardStateDictionary[key][0],
                    self.__boardStateDictionary[key][1]],
                    destination= [
                    self.__boardStateDictionary[key][0] + coordinate[0],
                    self.__boardStateDictionary[key][1] + coordinate[1]
                ])

                if self.__actionOutsideBoard(candidateAction) or self.__actionCausesPieceCollision(candidateAction):
                    continue

                actionList.append(candidateAction)
        return actionList

    def resultantStateAfterAction(self, action):
        boardStateDictionaryCopy = copy.deepcopy(self.__boardStateDictionary)
        if action.initialPosition == boardStateDictionaryCopy[action.piece]:
            boardStateDictionaryCopy[action.piece] = action.destination
        else:
            raise ValueError("Actions initial position doesn't match the current initial position of the piece in the board state dictionary!")
        return BoardState(boardStateDictionaryCopy)

    def boardPosStringId(self):
        return str(self.__boardPositionMatrix)

    def distanceToL1(self, otherState):

        manhattanDistance = 0
        for key in self.__boardStateDictionary:
            manhattanDistance += abs(otherState.__boardStateDictionary[key][0] - self.__boardStateDictionary[key][0]) + abs(otherState.__boardStateDictionary[key][1] - self.__boardStateDictionary[key][1])

        return manhattanDistance

    def distanceToL2(self, otherState):

        euclideanDistance = 0
        for key in self.__boardStateDictionary:
            euclideanDistance += ((otherState.__boardStateDictionary[key][0] - self.__boardStateDictionary[key][0])**2 + (otherState.__boardStateDictionary[key][1] - self.__boardStateDictionary[key][1])**2)**0.5

        return euclideanDistance


    def __str__(self):

        outputString = ""
        for i in range(self.__maxCoordinate, -1, -1):
            for j in range(self.__maxCoordinate + 1):
                if self.__boardPositionMatrix[j][i] is None:
                    outputString += "  " + "|"
                else:
                    outputString += self.__boardPositionMatrix[j][i] + "|"

            outputString += "\n"

        return outputString

    def __eq__(self, other):

        # The other object must be the same type as this one.
        if type(self) is not type(other):
            return False

        # Loop through all the keys in the board state dictionary of self object
        for key in self.__boardStateDictionary.keys():
            # The keys in both dictionaries are exactly the same. For them to be equal
            # all the values must match.
            if self.__boardStateDictionary[key] != other.__boardStateDictionary[key]:
                return False

        return True





