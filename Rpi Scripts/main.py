from piece_path_finding.board_state import BoardState
from piece_path_finding.piece_path_finding_config import boardStartStateDictionary, boardTestStateDictionary
from piece_path_finding.best_first_search import bestFirstSearch
from piece_path_finding.problem import Problem
from piece_path_finding.solution_handler import SolutionHandler

import copy

import tracemalloc

if __name__ == '__main__':
   tracemalloc.start()
   initialState = BoardState(boardStateDictionary=boardStartStateDictionary)
   print(initialState)

   boardGoalStateDictionary = copy.deepcopy(boardStartStateDictionary)


   boardGoalStateDictionary["P1"] = [6, 9]
   boardGoalStateDictionary["k0"] = [0, 2]




   goalState = BoardState(boardStateDictionary=boardGoalStateDictionary)
   print(goalState)

   problem = Problem(initialState=initialState, goalState=goalState)

   solutionNode = bestFirstSearch(problem)

   node = solutionNode

   testSolutionHandler = SolutionHandler(solutionNode)
   print(testSolutionHandler)
   testSolutionHandler.retrieveNeccesaryActions()
   #print(testSolutionHandler)
   _, peak = tracemalloc.get_traced_memory()
   tracemalloc.stop()

   print(str(peak/10**6) + " Mb")






