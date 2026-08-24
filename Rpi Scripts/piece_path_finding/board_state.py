import copy
import chess
from piece_path_finding.action import Action


class BoardState:
    """
    Stores the state of the board and all related functions for the board state that is stored inside the problem abstraction and used in the best first search algorithm. Furthermore, the board state is also utilized by the board manager classes.
    """

    # When checking for available actions I have to check right, left, up and down. Rather than doing this inside the
    # function and repeating logic I have created this variable so that I can just loop through it.
    __adjacentSquareHelper = [
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1]
    ]
    # The maximum and minimum coordinates on the board
    __maxCoordinate = 11
    __minCoordinate = 0

    def __init__(self, boardStateDictionary):
        """
        Initializes the board state object by taking a dictionary that has strings for the pieces and the value is the
        location of the piece.
        Args:
            boardStateDictionary: A dictionary that has strings for the pieces and the value is the location of the
            piece stored in a list with 2 elements with the first element being x position and the second the y position..
        Returns:

        """
        self.__boardStateDictionary = boardStateDictionary
        # Generates the current position of the board into 2d nested list
        self.__boardPositionMatrix = self.__generateBoardPositionMatrix()

    def __generateBoardPositionMatrix(self):
        """
        Generates a 2d matrix that has the board position. This is required because later we need to be able to check if
        specific squares are already occupied by a piece. To do this with the dictionary requires looping through all
        keys making it O(n) complexity with this method it becomes O(1). Howerver to make use of this it has to be used
        more than once because the creation of the nested list takes O(n).

        Returns:
            boardPositionMatrix: A 2d nested list that corresponds to the position of the board. The keys of the pieces
            are stored at thier corresponding [x][y] location within the list.

        """
        boardPositionMatrix = []

        # Generate the empty matrix
        for i in range(BoardState.__maxCoordinate + 1):
            boardPositionMatrix.append([None] * (BoardState.__maxCoordinate + 1))

        # Loop through all the keys in the dictionary putting the key at the corresponding x,y location
        for key in self.__boardStateDictionary.keys():
            x = self.__boardStateDictionary[key][0]
            y = self.__boardStateDictionary[key][1]
            boardPositionMatrix[x][y] = key

        return boardPositionMatrix

    def __actionOutsideBoard(self, action):
        """
        Determines whether an entered action lies outside of the board.
        Args:
             action: An action object that contains the piece that is being moved, its initial position and its
             destination position.
        Returns:
            A boolean with true mean that the action IS outside the dimensions of the board and false meaning that it
            is not.
        """
        # The destination of the piece is beyond the bounds of the baord then the piece lays outside the dimensions of
        # the board.
        if action.destination[0] > BoardState.__maxCoordinate or action.destination[1] > BoardState.__maxCoordinate or action.destination[
            0] < BoardState.__minCoordinate or action.destination[1] < BoardState.__minCoordinate:
            return True

        return False

    def __actionCausesPieceCollision(self, action):
        """
        Determines whether the action taken will lead to a collision.

        Args:
            action: An action object that contains the piece that is being moved, its initial position and its
            destination position.
        Returns:
            A boolean with true mean that the action is causing a collision.
        """
        # Extract the x and the y location of the destination.
        x = action.destination[0]
        y = action.destination[1]

        # If the position is not None then there is a piece in that location and thus the action causes a collision.
        if self.__boardPositionMatrix[x][y] is not None:
            return True

        return False

    def actions(self):
        """
        Determines the actions that are available in the current board state.

        Returns:
             A list of available actions.
        """
        # The list the will become the return value and stores all the actions.
        actionList = []

        # Loop through all the keys (pieces) in the board state dictionary
        for key in self.__boardStateDictionary.keys():
            # Loop through the adjacentSquareHelper thus checking all the available ways that the piece can move
            for coordinate in BoardState.__adjacentSquareHelper:
                # Constructions an action object at this stage it is just a candidate action and needs to be "vetted"
                # before it is allowed to become an actual available action.
                candidateAction = Action(piece=key,
                    initialPosition = [
                    self.__boardStateDictionary[key][0],
                    self.__boardStateDictionary[key][1]],
                    destination= [
                    self.__boardStateDictionary[key][0] + coordinate[0],
                    self.__boardStateDictionary[key][1] + coordinate[1]
                ])

                # If the candidate action is either outside the board or it causes a collision then it can not be an
                # action.
                if self.__actionOutsideBoard(candidateAction) or self.__actionCausesPieceCollision(candidateAction):
                    continue

                # Action has passed all the testing so we therefore append it to the list.
                actionList.append(candidateAction)
        return actionList

    def resultantStateAfterAction(self, action):
        """
        Takes an action and applys it to the current board state. This function returns a new boardState object leaving
        self UNALTERED
        Args:
            action: the action that is being applied to the current board state.
        Returns:
            a board state object that has the new state after the action has taken place.
        """
        # We have to create a deep copy of the board state dictionary so that changes made to the new board state
        # dictionary are not reflected in the old.
        boardStateDictionaryCopy = copy.deepcopy(self.__boardStateDictionary)

        # Checks that initial position of the piece in the action and in the current board state match. If they do match
        # then update the location of the piece in the copied board state dictionary to the location dicated by the
        # destination of the action. If they don't match raise a value error.
        if action.initialPosition == boardStateDictionaryCopy[action.piece]:
            boardStateDictionaryCopy[action.piece] = action.destination
        else:
            raise ValueError("Actions initial position doesn't match the current initial position of the piece in the board state dictionary!")
        return BoardState(boardStateDictionaryCopy)

    def boardPosStringId(self):
        """
        Takes the board position matrix and turns it into a string that can act as the id for the current board position
        this is needed in the best first search for the reached table. This becomes the key in the reached dictionary
        for the current board position.
        Return:
             the board position matrix turned into a string
        """
        return str(self.__boardPositionMatrix)

    def distanceToL1(self, otherState):
        """
        Calculates the L1 distance between the current board state and another board state. To do this it calculates the
        L1 distance between all pieces and sums this up.

        Args:
            otherState: The other state that we will be calculating the distance to.
        Returns:
            manhattanDistance: The manhattan distance between board states.
        """

        manhattanDistance = 0
        for key in self.__boardStateDictionary:
            manhattanDistance += abs(otherState.__boardStateDictionary[key][0] - self.__boardStateDictionary[key][0]) + abs(otherState.__boardStateDictionary[key][1] - self.__boardStateDictionary[key][1])

        return manhattanDistance

    def distanceToL2(self, otherState):
        """
        Calculates the L2 distance between the current board state and another board state. To do this it calculates the
        L2 distance between all pieces and sums this up.

        Args:
            otherState: The other state that we will be calculating the distance to.
        Returns:
            euclideanDistance: The manhattan distance between board states.
        """
        euclideanDistance = 0
        for key in self.__boardStateDictionary:
            euclideanDistance += ((otherState.__boardStateDictionary[key][0] - self.__boardStateDictionary[key][0])**2 + (otherState.__boardStateDictionary[key][1] - self.__boardStateDictionary[key][1])**2)**0.5

        return euclideanDistance

    def getPieceAtLocation(self, location):
        """
        Gets the piece at the given location
        Args:
            Location: the location to get the piece at
        Returns:
            The string representation of the piece at the given location
        """
        return self.__boardPositionMatrix[location[0]][location[1]]

    def findDeadPieceLocation(self, promotedPiecePrefix):
        x = 0
        for y in range(0, len(self.__boardPositionMatrix)):
            pieceAtLocation = self.__boardPositionMatrix[x][y]
            pieceAtLocationSuffix = pieceAtLocation[0]
            if pieceAtLocationSuffix == promotedPiecePrefix:
                return x, y

        y = len(self.__boardPositionMatrix)
        for x in range(0, len(self.__boardPositionMatrix)):
            pieceAtLocation = self.__boardPositionMatrix[x][y]
            pieceAtLocationSuffix = pieceAtLocation[0]
            if pieceAtLocationSuffix == promotedPiecePrefix:
                return x, y

        x = len(self.__boardPositionMatrix) - 1
        for y in range(0, len(self.__boardPositionMatrix)):
            pieceAtLocation = self.__boardPositionMatrix[x][y]
            pieceAtLocationSuffix = pieceAtLocation[0]
            if pieceAtLocationSuffix == promotedPiecePrefix:
                return x, y

        y = 0
        for x in range(0, len(self.__boardPositionMatrix)):
            pieceAtLocation = self.__boardPositionMatrix[x][y]
            pieceAtLocationSuffix = pieceAtLocation[0]
            if pieceAtLocationSuffix == promotedPiecePrefix:
                return x, y

        # None means the piece is not in the graveyard.
        return None

    def findFreeGraveSpace(self, victimColour):
        if victimColour == chess.WHITE:
            return self.__findFreeWhiteGraveSpace()
        elif victimColour == chess.BLACK:
            return self.__findFreeBlackGraveSpace()

    def __findFreeWhiteGraveSpace(self):
        x = 0
        for y in range(0, int(len(self.__boardPositionMatrix)/2)):
            if self.__boardPositionMatrix[x][y] is None:
                return [x, y]

        y = 0
        for x in range(0, len(self.__boardPositionMatrix)):
            if self.__boardPositionMatrix[x][y] is None:
                return [x, y]

        x = len(self.__boardPositionMatrix) - 1
        for y in range(0,  int(len(self.__boardPositionMatrix)/2)):
            if self.__boardPositionMatrix[x][y] is None:
                return [x, y]

        assert False, "There is no free white grave space! This should never happen!"

    def __findFreeBlackGraveSpace(self):
        x = 0
        for y in range(int(len(self.__boardPositionMatrix)/2), len(self.__boardPositionMatrix)):
            if self.__boardPositionMatrix[x][y] is None:
                return [x, y]

        y = len(self.__boardPositionMatrix) - 1
        for x in range(0, len(self.__boardPositionMatrix)):
            if self.__boardPositionMatrix[x][y] is None:
                return [x, y]

        x = len(self.__boardPositionMatrix) - 1
        for y in range(int(len(self.__boardPositionMatrix)/2), len(self.__boardPositionMatrix)):
            if self.__boardPositionMatrix[x][y] is None:
                return [x, y]

        assert False, "There is no free black grave space! This should never happen!"

    def __str__(self):
        """
        Returns the string representation of the current board state.
        """
        # The variable that will be returned as the output
        outputString = ""

        # All this logic just ensures that the output string presents properly so that in the terminal it shows a top-down
        # view of the board with white at the bottom and black at the top.
        for i in range(BoardState.__maxCoordinate, -1, -1):
            for j in range(BoardState.__maxCoordinate + 1):
                if self.__boardPositionMatrix[j][i] is None:
                    outputString += "  " + "|"
                else:
                    outputString += self.__boardPositionMatrix[j][i] + "|"
            outputString += "\n"

        return outputString

    def __eq__(self, other):
        """
        Determines whether the position of the board in this board state and another are the same.

        Args:
            other: The other board state to compare with.
        Returns:
            boolean with true meaning that the states and the same and false meaning that they ARE NOT the same.
        """
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





