from piece_path_finding.board_state import BoardState
from piece_path_finding.piece_path_finding_config import initialBoardStartStateDictionary, boardTestStateDictionary
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
   
   """
   tracemalloc.start()
   initialState = BoardState(boardStateDictionary=initialBoardStartStateDictionary)
   print(initialState)

   boardGoalStateDictionary = copy.deepcopy(initialBoardStartStateDictionary)


   boardGoalStateDictionary["N0"] = [3, 9]
   boardGoalStateDictionary["n0"] = [3, 2]





   goalState = BoardState(boardStateDictionary=boardGoalStateDictionary)
   print(goalState)

   problem = Problem(initialState=initialState, goalState=goalState)

   solutionNode = bestFirstSearch(problem)

   node = solutionNode

   testSolutionHandler = SolutionHandler(solutionNode)

   #testSolutionHandler.retrieveNeccesaryActions()
   print(testSolutionHandler)
   _, peak = tracemalloc.get_traced_memory()
   tracemalloc.stop()

   print(str(peak/10**6) + " Mb")
   outgoing = testSolutionHandler.getActionString()

   print(outgoing)
   print(f"The string being sent is {len(outgoing)} bytes long.")

   # Socket Client
   """
   socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   socket.connect((HOST, PORT))


   socket.send(outgoing.encode('utf-8'))

   incoming = socket.recv(1024).decode('utf-8')

   socket.send(outgoing.encode('utf-8'))

   incoming = socket.recv(1024).decode('utf-8')

   socket.send("END".encode('utf-8'))

   socket.close()
   """





