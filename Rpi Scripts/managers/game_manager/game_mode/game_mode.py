from abc import ABC, abstractmethod
from chess_adversarial_search.minimax_alpha_beta import timeBoundedMinimaxAlphaBetaSearch
import chess

class GameMode(ABC):
    """
    Base class for all game modes. The base class contains the functions that are required to run the different game modes.
    While the derived classes are simple and use the exposed protected methods of the base class to run the different game modes.
    """
    def __init__(self, boardManager, userInterface, maxSearchTimeSeconds):
        """
        The base class constructor for different game modes that initializes attributes needed by all base classes.
        Args:
            boardManager: A BoardManager object that enables communication with the robotic assembly.
            userInterface: A UserInterface object that provides a mean for the user to communicate with the game and enter
            moves ect.
            maxSearchTimeSeconds: The maximum number of seconds that the minimax algorithm will spend searching
        """
        self._boardManager = boardManager
        self._userInterface = userInterface
        self._maxSearchTimeSeconds = maxSearchTimeSeconds
        # The max search depth is set to 1000 (which is effectively unlimited). It is set during the difficulty select.
        # The reason it is set to 1000 here is because during the difficulty select if the maximum difficulty is selected
        # the alpha beta search becomes time bounded and not depth bounded so we essentially want it to continue searching
        # until the time runs out.
        self._maxSearchPlyDepth = 1000
        # Maps python chess colours to text colours because chess.BLACK = 0(False) and chess.WHITE = 1(True)
        self._chessColourAsText = ['black', 'white']

    @abstractmethod
    def playGameMode(self, chessBoard, game):
        """
        Function that is to be overridden by all subclasses. This function runs the different games modes.
        Args:
            chessBoard: A python chess board object.
            game: A Game object that is utilized by the alpha beta search. It contains all methods to search the game
            tree.
        """
        pass

    def selectDifficulty(self):
        """
        Gets the difficulty level of the robot from the user. Maps difficulty levels to different search ply depths.
        depths.
        """
        # List of acceptable difficulties as strings.
        acceptableDifficulties = {'1', '2', '3', '4', '5', '6'}
        # Loops until a valid selection is made by the user. (The mapping from difficulty to ply depth is also done in
        # this loop)
        while True:
            # Get the difficulty from the user through the user interface
            difficulty = self._userInterface.getDifficultyFromUser(displayScreen=[chess.WHITE, chess.BLACK])
            # If the difficulty is not valid prompt the user to reselect
            if difficulty not in acceptableDifficulties:
                self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                                text="You have selected an invalid difficulty level! Please Reselect!\n")
                continue
            # Only restrict the search ply depth if the difficulty is not 6 (6 is the maximum difficulty and is only time
            # bounded)
            if int(difficulty) >= 1 and int(difficulty) <= 5:
                self._maxSearchPlyDepth = int(difficulty) + 1
            break

    def endOfGame(self, chessBoard):
        """
        Handles the end of the game.
        Args:
            chessBoard: A python chess board object.
        """
        # Informs the user (through the user interface) of the outcome of the game.
        self.__gameResultInfo(chessBoard)
        # Displays an end game message on the physical chess board (this doesnt do anything at this stage can be added
        # later if desired)
        self._boardManager.gameEndMessage()
        # Inform the user of the upcoming actions
        self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                        text="Calculating and\nexecuting actions\nto reset board this\nmay take a while!")
        # Calculate the actions to get back to the start state and execute these actions
        self._boardManager.resetBoard()

    def _playerMove(self, chessBoard):
        """
        Gets the move from the player then executes that move.
        Args:
            chessBoard: A python chess board object.
        Returns:
            A boolean representing whether the game is over or not. With 'True' representing that it is and 'False' that
            is not.
        """
        # Tells the user whos move it is and displays the board state in the console
        self.__moveInfo(chessBoard)
        # Checks if a draw can be claimed and then gets the user to accept or decline the draw
        if self.__claimDraw(chessBoard):
            return True
        # Gets the move off the player (through the UI) and converts it to a python chess.MOVE object
        playerMove = chess.Move.from_uci(self.__playerSelectMove(chessBoard))
        # Executes the move on the board with the robotic assembly
        self._boardManager.executeMove(playerMove, chessBoard)
        # Execute the move on the python chessboard
        chessBoard.push(playerMove)
        # Give info about the move to the user through the UI
        self.__resultingMoveInfo(chessBoard, playerMove)
        # Check if the game is over
        if chessBoard.is_game_over():
            return True
        return False

    def _engineMove(self, chessBoard, game):
        """
        Calculates the engine move. Then executes it.
        Args:
            chessBoard: A python chess board object.
            game: A Game object that is utilized by the alpha beta search. It contains all methods to search the game
            tree.
        Returns:
            A boolean representing whether the game is over or not. With 'True' representing that it is and 'False' that
            is not.
        """
        # Tells the user whos move it is and displays the board state in the console
        self.__moveInfo(chessBoard)
        # Tell the user some more information about the engine move
        self.__informEngineMoveCalculationStart(chessBoard, self._maxSearchTimeSeconds)
        # Execute the minimax alphabeta search and get the move the engine has calculated.
        engineMove = timeBoundedMinimaxAlphaBetaSearch(game=game,
                                                       chessBoard=chessBoard,
                                                       maxSearchTimeSeconds=self._maxSearchTimeSeconds,
                                                       maxSearchPlyDepth=self._maxSearchPlyDepth)
        # Tell the user the engine has calculated the move
        self.__informEngineMoveCalculationEnd(chessBoard)
        # Execute the calculated engine move
        self._boardManager.executeMove(engineMove, chessBoard)
        # Execute the move on the python chessboard
        chessBoard.push(engineMove)
        # Give info about the move to the user through the UI
        self.__resultingMoveInfo(chessBoard, engineMove)
        # Check if the game is over
        if chessBoard.is_game_over():
            return True
        return False

    def __playerSelectMove(self, chessBoard):
        """
        Get the move off the player.
        Args:
            chessBoard: A python chess board object.
        Returns:
            selectedMove: A uci string representation of the move selected by the player.
        """
        selectedMove = None
        legalMoveMade = False
        # Only allows legal moves
        while not legalMoveMade:
            # Gets a move from the user (the user can enter illegal moves but they will be detected and checked)
            candidateMove = self._userInterface.getMoveFromUser(displayScreen=[chessBoard.turn])
            # Get a list of the available moves
            availableMoves = list(chessBoard.legal_moves)
            # The legal moves are a subset of the available moves. This is due to promotions because it is possible that
            # a promotion can occur but cant be supported because the piece is not available in the graveyard.
            legalMoves = []
            # Checks if the player selected promotion is supported
            for move in availableMoves:
                if (move.promotion) and (self._boardManager.promotionIsIllegal(move)):
                    continue
                legalMoves.append(move)
            # Confirms if the player has selected a legal move
            for move in legalMoves:
                if str(move) == candidateMove:
                    legalMoveMade = True
                    selectedMove = candidateMove
                    break
            # Inform the user through the user interface that the move they have made is illegal
            if not legalMoveMade:
                self._userInterface.displayText(displayScreen=[chessBoard.turn],
                                                text="The move that you have selected is illegal OR there is not enough material for the promotion requested! Please re-enter your move!",
                                                screenTextOveride="Illegal move OR\nnot enough material\nfor promotion.\nReselect Move!",
                                                delaySeconds=5)
        # Return the selected move
        return selectedMove
    
    def __informEngineMoveCalculationStart(self, chessBoard, maxSearchTimeSeconds):
        """
        Inform the user that the engine is going to start calculating its move. Also display a message on the robots screens.
        Args:
            chessBoard: A python chess board object.
            maxSearchTimeSeconds: Maximum search time of the alphabeta minimax search in seconds.
        """
        self._userInterface.displayText(displayScreen=[not(chessBoard.turn)],
                                        text=f"Robot oponent\ncalculating move!\nThis will take at\nmost {maxSearchTimeSeconds} seconds!",
                                        delaySeconds=0)

        self._userInterface.displayText(displayScreen=[chessBoard.turn],
                                        text=f"Calculating my move!",
                                        delaySeconds=2)
        
    def __informEngineMoveCalculationEnd(self, chessBoard):
        """
        Inform the user that the engine has calculated its move.
        Args:
            chessBoard: A python chess board object.
        """
        self._userInterface.displayText(displayScreen=[not(chessBoard.turn)],
                                        text=f"Opponent has\ncalculated move!\nExecuting move!",
                                        delaySeconds=0)
        self._userInterface.displayText(displayScreen=[chessBoard.turn],
                                        text=f"I've calculated my move!\nExcuting move!",
                                        delaySeconds=2)
        
    def __claimDraw(self, chessBoard):
        """
        Determines if the user can claim a draw and then gets the user to decide whether or not they want.
        Args:
            chessBoard: A python chess board object.
        """
        while chessBoard.can_claim_draw():
            # 50 moves without a capture or pawn move
            if chessBoard.can_claim_fifty_moves():
                # Get a yes or no answer from the user as to whether or not they want to claim a draw
                selection = self._userInterface.yesOrNoQuestion(displayScreen=[chessBoard.turn],
                                                                question="50 moves without a\ncapture or pawn move!\nClaim a draw?")
            # 3 repeated moves
            else:
                # Get a yes or no answer from the user as to whether or not they want to claim a draw
                selection = self._userInterface.yesOrNoQuestion(displayScreen=[chessBoard.turn],
                                                                question="3 positions have\nrepeated in the game!\nClaim a draw?")
            
            # The user does not want a draw
            if selection == "NO":
                return False
            # The user wants a draw
            elif selection == "YES":
                return True
            else:
                self._userInterface.displayText(displayScreen=[chessBoard.turn],
                                                text="The selection was not recognized. Please re-enter your selection!")
        return False

    def __moveInfo(self, chessBoard):
        """
        Displays to the user whos move it is. Also displays the board state in the console.
        Args:
            chessBoard: A python chess board object.
        """
        self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                        text=f"%%%%%%%%%%%%%%%%%%%%%%%\nIt is {self._chessColourAsText[chessBoard.turn]} turn to move.The state of the board is:\n{chessBoard}",
                                        screenTextOveride=f"It is {self._chessColourAsText[chessBoard.turn]} turn to move!",
                                        delaySeconds=2)

    def __resultingMoveInfo(self, chessBoard, move):
        """
        Displays the move made.
        Args:
            chessBoard: A python chess board object.
            move: A uci string representation of the move made.
        """
        self._userInterface.displayText(displayScreen=[chess.WHITE, chess.BLACK],
                                        text=f"The move made was: {move}.",
                                        screenTextOveride=f"The move made was:\n{move}",
                                        delaySeconds=2)

    def __gameResultInfo(self, chessBoard):
        """
        Displays the result of the game.
        Args:
            chessBoard: A python chess board object.
        """
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
    """
    The game mode for a white player and black robot.
    """
    def playGameMode(self, chessBoard, game):
        """
        The player moves first making it the white player and then the robot second making it the black robot.
        Args:
            chessBoard: A python chess board object.
            game: A Game object that is utilized by the alpha beta search. It contains all methods to search the game
            tree.
        """
        while True:
            if self._playerMove(chessBoard):
                break

            if self._engineMove(chessBoard, game):
                break

class BlackPlayerWhiteRobot(GameMode):
    """
        The game mode for a black player and white robot.
    """
    def playGameMode(self, chessBoard, game):
        """
        The robot moves first making it the white robot and then the player second making it the black player.
        Args:
            chessBoard: A python chess board object.
            game: A Game object that is utilized by the alpha beta search. It contains all methods to search the game
            tree.
        """
        while True:
            if self._engineMove(chessBoard, game):
                break

            if self._playerMove(chessBoard):
                break

class PlayerPlayer(GameMode):
    """
    The game mode for a player vs player.
    """
    def playGameMode(self, chessBoard, game):
        """
        Players continuously making moves.
        Args:
            chessBoard: A python chess board object.
            game: A Game object that is utilized by the alpha beta search. It contains all methods to search the game
            tree.
        """
        while True:
            if self._playerMove(chessBoard):
                break

    def selectDifficulty(self):
        """
        Select difficulty is overiden with an empty function. So that no difficulty is selected because it is obviously
        not needed for player vs player (theres no robot involved).
        """
        return None

class RobotRobot(GameMode):
    """
        The game mode for a robot vs robot.
    """
    def playGameMode(self, chessBoard, game):
        """
        Robot continuously making moves.
        Args:
            chessBoard: A python chess board object.
            game: A Game object that is utilized by the alpha beta search. It contains all methods to search the game
            tree.
        """
        while True:
            if self._engineMove(chessBoard, game):
                break