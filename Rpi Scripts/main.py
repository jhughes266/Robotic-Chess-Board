from piece_path_finding.board_state import BoardState
from piece_path_finding.piece_path_finding_config import boardStartStateDictionary

import copy

if __name__ == '__main__':
   boardState1 = BoardState(boardStateDictionary=boardStartStateDictionary)
   print(boardState1)
   print(boardState1.boardPosStringId())

   testAction = boardState1.actions()[0]
   print(testAction)
   boardState2 = boardState1.resultantStateAfterAction(testAction)
   print(boardState2)
   print(boardState2.boardPosStringId())





