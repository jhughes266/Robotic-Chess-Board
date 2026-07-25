from piece_path_finding.board_state import BoardState
from piece_path_finding.piece_path_finding_config import boardStartStateDictionary, boardTestStateDictionary
from piece_path_finding.best_first_search import bestFirstSearch
from piece_path_finding.problem import Problem

import copy

import tracemalloc

if __name__ == '__main__':
   tracemalloc.start()
   initialState = BoardState(boardStateDictionary=boardTestStateDictionary)
   print(initialState)

   boardGoalStateDictionary = copy.deepcopy(boardTestStateDictionary)


   boardGoalStateDictionary["P1"] = [7, 3]
   #boardGoalStateDictionary["k0"] = [0, 2]




   goalState = BoardState(boardStateDictionary=boardGoalStateDictionary)
   print(goalState)

   problem = Problem(initialState=initialState, goalState=goalState)

   solutionNode = bestFirstSearch(problem)

   node = solutionNode
   solutionList = []
   while node.parent is not None:
      solutionList.append(node)
      node = node.parent

   solutionList.reverse()

   for i, node in enumerate(solutionList):
      print("Action number: " + str(i+1))
      print(node.action)
      print(node.state)
      print("-------------------------------")

   _, peak = tracemalloc.get_traced_memory()
   tracemalloc.stop()

   print(str(peak/10**6) + " Mb")






