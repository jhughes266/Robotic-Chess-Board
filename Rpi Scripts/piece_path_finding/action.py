
class Action:

    def __init__(self, piece, destination):
        self.piece = piece
        self.destination = destination

    def __str__(self):
        return str(self.piece) + " : " + str(self.destination)