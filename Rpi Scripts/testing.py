import chess
from chess_adversarial_search.game import Game
from chess_adversarial_search.minimax_alpha_beta import timeBoundedMinimaxAlphaBetaSearch
testFen = '8/8/8/1P6/2KN2k1/8/8/8 w - - 0 1'
chessBoard = chess.Board()
game = Game()
while not chessBoard.is_game_over():

    engineMove = timeBoundedMinimaxAlphaBetaSearch(game, chessBoard, maxSearchTimeSeconds=5)
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
    #engineMove = minimaxAlphaBetaSearch(game, chessBoard)
    #chessBoard.push(engineMove)
    print("##############################################")
    print("BLACKS MOVE")
    print(chessBoard)
    print("##############################################")




print("end")