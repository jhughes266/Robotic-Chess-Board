testStr = '[2,3]E[1,3]D[3,3]E[2,3]D[5,5]E[5,4]D[9,3]E[11,3]D[2,2]E[0,2]D[9,2]E[11,2]D[4,2]E[3,2]D[6,3]E[6,2]D[2,8]E[1,8]D[3,8]E[2,8]D[4,8]E[3,8]D[9,8]E[10,8]D[8,8]E[9,8]D[7,8]E[8,8]D[10,8]E[11,8]D[2,9]E[0,9]D[9,9]E[11,9]D[5,3]E[6,3]D[5,4]E[5,3]D[0,6]E[1,6]D[0,5]E[1,5]D[0,4]E[1,4]D[6,3]E[7,3]D[1,6]E[2,6]D[1,5]E[4,5]D[3,6]E[3,5]D[2,6]E[3,6]D[6,4]E[6,5]D[1,4]E[2,4]D[7,3]E[8,3]D[3,6]E[4,6]D[3,5]E[3,4]D[5,7]E[6,7]D[5,6]E[5,8]D[3,7]E[4,7]D[4,5]E[5,5]D[9,5]E[8,5][8,6]D[5,5]E[5,4][6,4]D[8,6]E[7,6][7,7]D[4,4]E[4,3][3,3]D[6,4]E[7,4][7,3]D[7,7]E[7,8][6,8]D[4,7]E[5,7]D[3,4]E[4,4][4,3]D[4,6]E[5,6]D[0,7]E[1,7]D[6,7]E[7,7][7,8]D[6,5]E[7,5][7,6]D[6,6]E[6,5]D[7,6]E[7,7]D[6,5]E[7,5][7,4]D[7,7]E[8,7]D[2,4]E[3,4]D[8,4]E[9,4][9,3]D[7,4]E[8,4]D[8,3]E[8,2]D[8,4]E[8,3]D[8,2]E[9,2]D[7,3]E[7,2][8,2]D[4,3]E[4,2][5,2]D[7,8]E[7,9][8,9]D[6,8]E[6,9][5,9]D[5,6]E[6,6][6,8]D[1,7]E[2,7]D[8,7]E[9,7]D[5,7]E[6,7]D[0,3]E[0,4]D[1,3]E[0,3]D[0,4]E[2,4]D[9,7]E[10,7][10,9][9,9]D[6,7]E[7,7][7,9][6,9]D[2,4]E[2,5][5,5][5,4][6,4][6,3]D[1,8]E[1,9]D[0,8]E[1,8][1,7]D[1,9]E[1,8][0,8]D[1,7]E[1,9][3,9]D[2,7]E[1,7][1,9][2,9]D[3,3]E[4,3]D[3,4]E[3,3]D[4,3]E[4,1][2,1][2,2]D'

class PieceMover:
    def __init__(self):
        pass

    def moveToGridXY(self, gridX, gridY):
        pass

    def engageGripper(self):
        pass

    def disengageGripper(self):
        pass



def excuteCommand(command, pieceMover, mode="real"):
    """
    This function takes a command in string form that is read and then excuted by
    the pico causing the robotic assembly to move.
    Args:
        command: A string that contains the commands for the robot and will parsed
        and have the commands extracted and exectued.
        pieceMover: A piece mover object that allows the function to move the
        robotic assembly.
        mode: The mode can be "fake" or "real". Fake is for when the robot is not connected
        it allows the pico to send messages mimicing that it has moved to the correct
        location. Real will move the robotic assembly.
    Returns:

    """
    # The mode is fake so we just bypass the function.
    if mode == "fake":
        print("Mode is fake. This message is to signify a mock moving of the pieces. Returning from function!")
        return

    # First we disengage the gripper to make sure it wont interfer with any pieces
    pieceMover.disengageGripper()

    i = 0
    while i < len(command):

        character = command[i]
        gridX, gridY = None, None

        if character == "[":
            j = i
            posStr = ""
            while True:
                j += 1
                if command[j] == ",":
                    gridX = int(posStr)
                    posStr = ""
                    continue
                elif command[j] == "]":
                    gridY = int(posStr)
                    break
                posStr += command[j]

            pieceMover.moveToGridXY(gridX, gridY)
        elif character == "E":
            pieceMover.engageGripper()
        elif character == "D":
            pieceMover.disengageGripper()

        i += 1
pieceMover = PieceMover()
excuteCommand(command=testStr, pieceMover=pieceMover)

"""
import chess
from chess_adversarial_search.game_manager import Game
from chess_adversarial_search.minimax_alpha_beta import timeBoundedMinimaxAlphaBetaSearch
testFen = '8/8/8/1P6/2KN2k1/8/8/8 w - - 0 1'
chessBoard = chess.Board()
game_manager = Game()
while not chessBoard.is_game_over():

    engineMove = timeBoundedMinimaxAlphaBetaSearch(game_manager, chessBoard, maxSearchTimeSeconds=5)
    chessBoard.push(engineMove)
    print("##############################################")
    print("WHITES MOVE")
    print(engineMove)
    print(chessBoard)
    print("##############################################")
    legalMoveMade = False
    while legalMoveMade == False:
     move = input("Select move: ")
     legalMoves = list(chessBoard.legal_moves)
     for legalMove in legalMoves:
        if move == str(legalMove):
           legalMoveMade = True
    playerMove = chess.Move.from_uci(move)
    chessBoard.push(playerMove)
    #engineMove = minimaxAlphaBetaSearch(game_manager, chessBoard)
    #chessBoard.push(engineMove)
    print("##############################################")
    print("BLACKS MOVE")
    print(chessBoard)
    print("##############################################")




print("end")
"""