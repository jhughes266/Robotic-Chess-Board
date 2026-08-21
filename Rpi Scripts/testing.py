import chess
from chess_adversarial_search.game import Game
from chess_adversarial_search.minimax_alpha_beta import minimaxAlphaBetaSearch
testFen = '4R3/3N3k/5R2/8/6P1/P3K3/1PP2P2/8 w - - 13 57'
chessBoard = chess.Board(testFen)
game = Game()
while not chessBoard.is_game_over():

    engineMove = minimaxAlphaBetaSearch(game, chessBoard, maxPlyDepth=5)
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