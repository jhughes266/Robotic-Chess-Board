from abc import ABC, abstractmethod
from chess_adversarial_search.minimax_alpha_beta import timeBoundedMinimaxAlphaBetaSearch
import chess

class GameMode(ABC):
    def __init__(self, boardManager, userInterface, maxSearchTimeSeconds):
        self._boardManager = boardManager
        self._userInterface = userInterface
        self._maxSearchTimeSeconds = maxSearchTimeSeconds
        self._maxSearchPlyDepth = 1000
        self._chessColourAsText = ['black', 'white']


    @abstractmethod
    def playGameMode(self, chessBoard, game):
        pass

    def selectDifficulty(self):
        acceptableDifficulties = {'1', '2', '3', '4', '5', '6'}
        while True:
            difficulty = self._userInterface.getDifficultyFromUser(displayScreen=[chess.WHITE, chess.BLACK])
            
            if difficulty not in acceptableDifficulties:
                self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                                text="You have selected an invalid difficulty level! Please Reselect!\n")
                continue

            if int(difficulty) >= 1 and int(difficulty) <= 5:
                self._maxSearchPlyDepth = int(difficulty) + 1
            break

    def endOfGame(self, chessBoard):
        self.__gameResultInfo(chessBoard)
        self._boardManager.gameEndMessage()
        self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                        text="Calculating and\nexecuting actions\nto reset board this\nmay take a while!")
        self._boardManager.resetBoard()

    def _playerMove(self, chessBoard):
        self.__moveInfo(chessBoard)
        if self.__claimDraw(chessBoard):
            return True
        playerMove = chess.Move.from_uci(self.__playerSelectMove(chessBoard))
        # Here we will free up the camera and the pose detection resources
        self._boardManager.executeMove(playerMove, chessBoard)
        chessBoard.push(playerMove)
        self.__resultingMoveInfo(chessBoard, playerMove)
        if chessBoard.is_game_over():
            return True
        return False

    def _engineMove(self, chessBoard, game):
        self.__moveInfo(chessBoard)
        self.__informEngineMoveCalculationStart(chessBoard, self._maxSearchTimeSeconds)
        engineMove = timeBoundedMinimaxAlphaBetaSearch(game=game,
                                                       chessBoard=chessBoard,
                                                       maxSearchTimeSeconds=self._maxSearchTimeSeconds,
                                                       maxSearchPlyDepth=self._maxSearchPlyDepth)
        self.__informEngineMoveCalculationEnd(chessBoard)
        self._boardManager.executeMove(engineMove, chessBoard)
        chessBoard.push(engineMove)
        self.__resultingMoveInfo(chessBoard, engineMove)
        if chessBoard.is_game_over():
            return True
        return False

    def __playerSelectMove(self, chessBoard):
        selectedMove = None
        legalMoveMade = False
        while not legalMoveMade:
            candidateMove = self._userInterface.getMoveFromUser(displayScreen=[chessBoard.turn])
            availableMoves = list(chessBoard.legal_moves)
            legalMoves = []

            # Checks if the player selected promotion is supported
            for move in availableMoves:
                if (move.promotion) and (self._boardManager.promotionIsIllegal(move)):
                    continue
                legalMoves.append(move)

            for move in legalMoves:
                if str(move) == candidateMove:
                    legalMoveMade = True
                    selectedMove = candidateMove
                    break

            if not legalMoveMade:
                self._userInterface.displayText(displayScreen=[chessBoard.turn],
                                                text="The move that you have selected is illegal OR there is not enough material for the promotion requested! Please re-enter your move!",
                                                screenTextOveride="Illegal move OR\nnot enough material\nfor promotion.\nReselect Move!",
                                                delaySeconds=5)
        return selectedMove
    
    def __informEngineMoveCalculationStart(self, chessBoard, maxSearchTimeSeconds):
        self._userInterface.displayText(displayScreen=[not(chessBoard.turn)],
                                        text=f"Robot oponent\ncalculating move!\nThis will take at\nmost {maxSearchTimeSeconds} seconds!",
                                        delaySeconds=0)
        self._userInterface.displayText(displayScreen=[chessBoard.turn],
                                        text=f"Calculating my move!",
                                        delaySeconds=2)
        
    def __informEngineMoveCalculationEnd(self, chessBoard):
        self._userInterface.displayText(displayScreen=[not(chessBoard.turn)],
                                        text=f"Opponent has\ncalculated move!\nExecuting move!",
                                        delaySeconds=0)
        self._userInterface.displayText(displayScreen=[chessBoard.turn],
                                        text=f"I've calculated my move!\nExcuting move!",
                                        delaySeconds=2)
        
    def __claimDraw(self, chessBoard):
        while chessBoard.can_claim_draw():
            if chessBoard.can_claim_fifty_moves():
                selection = self._userInterface.yesOrNoQuestion(displayScreen=[chessBoard.turn],
                                                                question="50 moves without a\ncapture or pawn move!\nClaim a draw?")
            else:
                selection = self._userInterface.yesOrNoQuestion(displayScreen=[chessBoard.turn],
                                                                question="3 positions have\nrepeated in the game!\nClaim a draw?")
            
           
            if selection == "NO":
                return False
            elif selection == "YES":
                return True
            else:
                self._userInterface.displayText(displayScreen=[chessBoard.turn],
                                                text="The selection was not recognized. Please re-enter your selection!")
        return False

    def __moveInfo(self, chessBoard):
        self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                        text=f"%%%%%%%%%%%%%%%%%%%%%%%\nIt is {self._chessColourAsText[chessBoard.turn]} turn to move.The state of the board is:\n{chessBoard}",
                                        screenTextOveride=f"It is {self._chessColourAsText[chessBoard.turn]} turn to move!",
                                        delaySeconds=2)

    def __resultingMoveInfo(self, chessBoard, move):
        self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                        text=f"The move made was {move}.\nThe state of the board after this move is:\n{str(chessBoard)}\n%%%%%%%%%%%%%%%%%%%%%%%",
                                        screenTextOveride=f"The move made was:\n{move}",
                                        delaySeconds=2)

    def __gameResultInfo(self, chessBoard):
        resultStr = chessBoard.result()
        if resultStr == '1-0':
            # White wins
            self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                            text="White Wins!\n\n\n",
                                            delaySeconds=5)
        elif resultStr == '0-1':
            # Black wins
            self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                            text="Black Wins!\n\n\n",
                                            delaySeconds=5)
        else:
            self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                            text="Game drawn!\n\n\n",
                                            delaySeconds=5)

class WhitePlayerBlackRobot(GameMode):
    def playGameMode(self, chessBoard, game):
        while True:
            if self._playerMove(chessBoard):
                break

            if self._engineMove(chessBoard, game):
                break

class BlackPlayerWhiteRobot(GameMode):
    def playGameMode(self, chessBoard, game):
        while True:
            if self._engineMove(chessBoard, game):
                break

            if self._playerMove(chessBoard):
                break

class PlayerPlayer(GameMode):
    def playGameMode(self, chessBoard, game):
        while True:
            if self._playerMove(chessBoard):
                break

    def selectDifficulty(self):
        return None

class RobotRobot(GameMode):
    def playGameMode(self, chessBoard, game):
        while True:
            if self._engineMove(chessBoard, game):
                break