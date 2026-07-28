
class Action:
    """
    Stores actions that are used for the best first search algorithm.
    """
    def __init__(self, piece, initialPosition, destination):
        """
        Initializes the action object.
        Args:
             piece: The string that represents the piece that is being moved.
             initialPosition: The initial position of the piece.
             destination: The destination position of the piece.
        """
        self.piece = piece
        self.initialPosition = initialPosition
        self.destination = destination

    def __str__(self):
        """
        Returns the string representation of the action.
        Returns:
             A string representing the action.
        """
        return str(self.piece) + " : " + str(self.initialPosition) + " --> " + str(self.destination)