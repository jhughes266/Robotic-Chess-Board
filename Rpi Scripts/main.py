from piece_path_finding.board_state import BoardState
from piece_path_finding.piece_path_finding_config import boardStartStateDictionary, boardTestStateDictionary
from piece_path_finding.best_first_search import bestFirstSearch
from piece_path_finding.problem import Problem
from piece_path_finding.solution_handler import SolutionHandler
from secrets import HOST, PORT
import copy
import tracemalloc
import socket
import chess
from chess_adversarial_search.game import Game
from chess_adversarial_search.minimax_alpha_beta import minimaxAlphaBetaSearch


if __name__ == '__main__':
   """
   chessBoard = chess.Board()
   game = Game()
   while not chessBoard.is_game_over():
      engineMove = minimaxAlphaBetaSearch(game, chessBoard, maxPlyDepth=6)
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
   """
   tracemalloc.start()
   initialState = BoardState(boardStateDictionary=boardStartStateDictionary)
   print(initialState)

   boardGoalStateDictionary = copy.deepcopy(boardStartStateDictionary)


   boardGoalStateDictionary["N1"] = [7, 4]




   goalState = BoardState(boardStateDictionary=boardGoalStateDictionary)
   print(goalState)

   problem = Problem(initialState=initialState, goalState=goalState)

   solutionNode = bestFirstSearch(problem)

   node = solutionNode

   testSolutionHandler = SolutionHandler(solutionNode)

   #testSolutionHandler.retrieveNeccesaryActions()
   #print(testSolutionHandler)
   _, peak = tracemalloc.get_traced_memory()
   tracemalloc.stop()

   print(str(peak/10**6) + " Mb")

   # Socket Client

   socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   socket.connect((HOST, PORT))

   outgoing = testSolutionHandler.getActionString()

   print(outgoing)
   print(f"The string being sent is {len(outgoing)} bytes long.")
   socket.send(outgoing.encode('utf-8'))

   incoming = socket.recv(1024).decode('utf-8')

   socket.send("END".encode('utf-8'))

   socket.close()






