
class Action:

    def __init__(self, piece, initialPosition, destination):
        self.piece = piece
        self.initialPosition = initialPosition
        self.destination = destination

    def __str__(self):
        return str(self.piece) + " : " + str(self.initialPosition) + " --> " + str(self.destination)