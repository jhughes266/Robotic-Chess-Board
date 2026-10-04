from piece_path_finding.board_state import BoardState
from piece_path_finding.piece_path_finding_config import initialBoardStartStateDictionary, intermediateBoardEndStateDictionary
from piece_path_finding.action import Action
from piece_path_finding.best_first_search import bestFirstSearch
from piece_path_finding.problem import Problem
from piece_path_finding.solution_handler import SolutionHandler
import chess

class BoardManager:
    """
    A class that manages the physical chess board. This includes move execution and operations that deal with the state of the board
    """
    def __init__(self, communicationManager):
        """
        Initializes the BoardManager object.
        Args:
             communicationManager: A communicationManager object that is responsible for communicating with the pico
             which controls the robotics portion of the project.
        """
        self.__communicationManager = communicationManager
        # Gives the ability to load a board state into the board. At the current time does nothing
        self._boardState = self._loadBoardState()
        # Loads the default initial position if no board state was loaded
        if self._boardState is None:
            self._boardState = BoardState(boardStateDictionary=initialBoardStartStateDictionary)

    def _chessSquareToBoardGridXY(self, square):
        """
        Takes a string representation of the square and converts into a grid coordinate on the board.
        Args:
            square: A string representation of a square on the chess board eg 'e3'.
        Returns:
            A list with the gridX position as the 0th element and the gridY position as the 1st element.
        """

        file = square[0]
        rank = square[1]
        gridX = ord(file) - 95
        gridY = int(rank) + 1
        return [gridX, gridY]

    def _loadBoardState(self):
        """
        Empty function that can be used to load a board state.
        """
        return None

    def promotionIsIllegal(self, move):
        """
        Checks if a promotion is illegal in terms of material in the graveyard. For example a promotion may be
        theoretically legal but if the piece is not in the graveyard it cant be allowed to occur (this wont happen
        often)
        Args:
            move: The move in uci form to be tested
        Returns:
            A boolean indicating if the promotion is illegal or not
        """
        # Gets the prefix of the piece that is to be promoted.
        promotedPiecePrefix = move.uci()[4]
        # If the piece can be found in the graveyard then the promotion is not illegal.
        if self._boardState.findDeadPieceLocation(promotedPiecePrefix) is not None:
            return False
        return True

    def executeMove(self, move, chessBoard):
        """
        Takes a move and a python chess board object and executes the move by sending commands to the pico.
        Args:
            move: The move in uci form to be executed.
            chessBoard: A python chess board object.
        """
        goalBoardState = None
        # Get the grid positions of the initial and destination positions.
        initialPosition = self._chessSquareToBoardGridXY(move.uci()[0:2])
        destinationPosition = self._chessSquareToBoardGridXY(move.uci()[2:4])
        # The goal board state needs to be carefully constructed. There are various different types of moves that involve
        # moving pieces to different locations. For example enpassant is different to a traditional capture because the
        # victim piece isnt located at the destination of the attacker. The functions that return the goal board state
        # are explained within this class in more depth in their respective definitions.
        # 1. A pawn promotion that is also a capture.
        if ((move.promotion is not None) and chessBoard.is_capture(move)):
            goalBoardState = self.__promotionAndCapture(move, chessBoard, initialPosition, destinationPosition)
        # 2. En passant
        elif chessBoard.is_en_passant(move):
            goalBoardState = self.__enPassant(move, chessBoard, initialPosition, destinationPosition)
        # 3. Capture
        elif chessBoard.is_capture(move):
            goalBoardState = self.__capture(move, chessBoard, initialPosition, destinationPosition)
        # 4. Promotion (no capture)
        elif move.promotion is not None:
            goalBoardState = self.__promotion(move, chessBoard, initialPosition, destinationPosition)
        # 5. Kingside castle
        elif chessBoard.is_kingside_castling(move):
            goalBoardState = self.__kingsideCastle(move, chessBoard, initialPosition, destinationPosition)
        # 6. Queenside castle
        elif chessBoard.is_queenside_castling(move):
            goalBoardState = self.__queensideCastle(move, chessBoard, initialPosition, destinationPosition)
        # 7. Regular move no capture going from one square to another
        else:
            goalBoardState = self.__normalMove(move, chessBoard, initialPosition, destinationPosition)

        actionString = self.__findActionString(initialState=self._boardState, goalState=goalBoardState)
        self._boardState = goalBoardState
        self.__communicationManager.executeCommand(actionString, maxCommandSize=20)
    # PLEASE NOTE IN THE BELOW FUNCTIONS WHEN I SAY 'MOVE' I MEAN GET THE BOARD STATE THAT RESULTS FROM THE MOVE
    def __promotionAndCapture(self, move, chessBoard, initialPosition, destinationPosition):
        """
        Takes a promotion and capture move and gets the goal board state from this promotion capture.
        Args:
            move: The move in uci form to be executed.
            chessBoard: A python chess board object.
            initialPosition: The initial position of the piece that is being moved.
            destinationPosition: The destination position of the piece that is being moved.
        """
        # We first move the pawn that is being promoted to the graveyard.
        pawnInitialPosition = initialPosition
        # The pawn is from the player who is moving
        pawnColour = chessBoard.turn
        pawnDestinationPosition = self._boardState.findFreeGraveSpace(pawnColour)
        pawnPiece = self._boardState.getPieceAtLocation(pawnInitialPosition)
        pawnKillAction = Action(piece=pawnPiece, initialPosition=pawnInitialPosition,
                                destination=pawnDestinationPosition)
        goalBoardState = self._boardState.resultantStateAfterAction(pawnKillAction)

        # We next move the victim piece to the graveyard.
        victimInitialPosition = destinationPosition
        # The move hasn't been executed yet so it is the attackers turn. So the opposite colour is the victim
        victimColour = not (chessBoard.turn)
        victimDestinationPosition = goalBoardState.findFreeGraveSpace(victimColour)
        victimPiece = goalBoardState.getPieceAtLocation(victimInitialPosition)
        victimAction = Action(piece=victimPiece, initialPosition=victimInitialPosition,
                              destination=victimDestinationPosition)
        goalBoardState = goalBoardState.resultantStateAfterAction(victimAction)

        # We then move the promoted piece from the graveyard to its promotion location on the board.
        promotedPiecePrefix = move.uci()[4]
        colourOfPromotedPiece = chessBoard.turn
        if colourOfPromotedPiece == chess.WHITE:
            promotedPiecePrefix = promotedPiecePrefix.upper()
        promotedInitialPosition = goalBoardState.findDeadPieceLocation(promotedPiecePrefix)
        promotedPiece = goalBoardState.getPieceAtLocation(promotedInitialPosition)
        promotedDestinationPosition = destinationPosition
        promotionAction = Action(piece=promotedPiece, initialPosition=promotedInitialPosition,
                                 destination=promotedDestinationPosition)
        goalBoardState = goalBoardState.resultantStateAfterAction(promotionAction)
        return goalBoardState

    def __capture(self, move, chessBoard, initialPosition, destinationPosition):
        """
        Takes a promotion and capture move and gets the goal board state from this promotion capture.
        Args:
            move: The move in uci form to be executed.
            chessBoard: A python chess board object.
            initialPosition: The initial position of the piece that is being moved.
            destinationPosition: The destination position of the piece that is being moved.
        """
        # Move the victim to the graveyard
        victimInitialPosition = destinationPosition
        # The move hasn't been executed yet so it is the attackers turn. So the opposite colour is the victim
        victimColour = not (chessBoard.turn)
        victimDestinationPosition = self._boardState.findFreeGraveSpace(victimColour)
        victimPiece = self._boardState.getPieceAtLocation(victimInitialPosition)
        victimAction = Action(piece=victimPiece, initialPosition=victimInitialPosition,
                              destination=victimDestinationPosition)
        goalBoardState = self._boardState.resultantStateAfterAction(victimAction)

        # Move the attacker to the destination square
        attackerInitialPosition = initialPosition
        attackerDestinationPosition = destinationPosition
        attackingPiece = goalBoardState.getPieceAtLocation(attackerInitialPosition)
        attackerAction = Action(piece=attackingPiece, initialPosition=attackerInitialPosition,
                                destination=attackerDestinationPosition)
        goalBoardState = goalBoardState.resultantStateAfterAction(attackerAction)
        return goalBoardState

    def __promotion(self, move, chessBoard, initialPosition, destinationPosition):
        """
        Takes a promotion move and gets the goal board state from this promotion.
        Args:
            move: The move in uci form to be executed.
            chessBoard: A python chess board object.
            initialPosition: The initial position of the piece that is being moved.
            destinationPosition: The destination position of the piece that is being moved.
        """
        # Move the pawn that is involved in the promotion to the graveyard
        pawnInitialPosition = initialPosition
        # The pawn is from the player who is moving
        pawnColour = chessBoard.turn
        pawnDestinationPosition = self._boardState.findFreeGraveSpace(pawnColour)
        pawnPiece = self._boardState.getPieceAtLocation(pawnInitialPosition)
        pawnKillAction = Action(piece=pawnPiece, initialPosition=pawnInitialPosition,
                                destination=pawnDestinationPosition)
        goalBoardState = self._boardState.resultantStateAfterAction(pawnKillAction)

        # Move the promoted piece from the graveyard to its location
        promotedPiecePrefix = move.uci()[4]
        colourOfPromotedPiece = chessBoard.turn
        if colourOfPromotedPiece == chess.WHITE:
            promotedPiecePrefix = promotedPiecePrefix.upper()
        promotedInitialPosition = goalBoardState.findDeadPieceLocation(promotedPiecePrefix)
        promotedPiece = goalBoardState.getPieceAtLocation(promotedInitialPosition)
        promotedDestinationPosition = destinationPosition
        promotionAction = Action(piece=promotedPiece, initialPosition=promotedInitialPosition,
                                 destination=promotedDestinationPosition)
        goalBoardState = goalBoardState.resultantStateAfterAction(promotionAction)
        return goalBoardState

    def __kingsideCastle(self, move, chessBoard, initialPosition, destinationPosition):
        """
        Takes a kingside castle move and gets the goal board state from this kingside castle.
        Args:
            move: The move in uci form to be executed.
            chessBoard: A python chess board object.
            initialPosition: The initial position of the piece that is being moved.
            destinationPosition: The destination position of the piece that is being moved.
        """
        # Move the king to its destination
        kingInitialPosition = initialPosition
        kingDestinationPosition = destinationPosition
        piece = self._boardState.getPieceAtLocation(kingInitialPosition)
        action = Action(piece=piece, initialPosition=kingInitialPosition, destination=kingDestinationPosition)
        goalBoardState = self._boardState.resultantStateAfterAction(action)

        # Move the rook to its destination
        rookInitialPosition = kingInitialPosition[:]
        rookInitialPosition[0] += 3
        rookDestinationPosition = kingInitialPosition[:]
        rookDestinationPosition[0] += 1
        piece = goalBoardState.getPieceAtLocation(rookInitialPosition)
        action = Action(piece=piece, initialPosition=rookInitialPosition, destination=rookDestinationPosition)
        goalBoardState = goalBoardState.resultantStateAfterAction(action)
        return goalBoardState

    def __queensideCastle(self, move, chessBoard, initialPosition, destinationPosition):
        """
        Takes a queenside castle move and gets the goal board state from this queenside castle.
        Args:
            move: The move in uci form to be executed.
            chessBoard: A python chess board object.
            initialPosition: The initial position of the piece that is being moved.
            destinationPosition: The destination position of the piece that is being moved.
        """
        # Move the king to its destination
        kingInitialPosition = initialPosition
        kingDestinationPosition = destinationPosition
        piece = self._boardState.getPieceAtLocation(kingInitialPosition)
        action = Action(piece=piece, initialPosition=kingInitialPosition, destination=kingDestinationPosition)
        goalBoardState = self._boardState.resultantStateAfterAction(action)

        # Move the rook to its destination
        rookInitialPosition = kingInitialPosition[:]
        rookInitialPosition[0] -= 4
        rookDestinationPosition = kingInitialPosition[:]
        rookDestinationPosition[0] -= 1
        piece = goalBoardState.getPieceAtLocation(rookInitialPosition)
        action = Action(piece=piece, initialPosition=rookInitialPosition, destination=rookDestinationPosition)
        goalBoardState = goalBoardState.resultantStateAfterAction(action)
        return goalBoardState

    def __enPassant(self, move, chessBoard, initialPosition, destinationPosition):
        """
        Takes an en passant move and gets the goal board state from this en passant.
        Args:
            move: The move in uci form to be executed.
            chessBoard: A python chess board object.
            initialPosition: The initial position of the piece that is being moved.
            destinationPosition: The destination position of the piece that is being moved.
        """
        # Move the victim pawn to its graveyard location
        # There needs to be an offset because the pawn is either up or down depending on the capturing side.
        victimYOffset = -1
        if chessBoard.turn == chess.BLACK:
            victimYOffset = +1
        victimInitialPosition = destinationPosition[:]
        victimInitialPosition[1] += victimYOffset
        # The move hasn't been executed yet so it is the attackers turn. So the opposite colour is the victim
        victimColour = not (chessBoard.turn)
        victimDestinationPosition = self._boardState.findFreeGraveSpace(victimColour)
        victimPiece = self._boardState.getPieceAtLocation(victimInitialPosition)
        victimAction = Action(piece=victimPiece, initialPosition=victimInitialPosition,
                              destination=victimDestinationPosition)
        goalBoardState = self._boardState.resultantStateAfterAction(victimAction)

        # Move the attacker to its destination location.
        attackerInitialPosition = initialPosition
        attackerDestinationPosition = destinationPosition
        attackingPiece = goalBoardState.getPieceAtLocation(attackerInitialPosition)
        attackerAction = Action(piece=attackingPiece, initialPosition=attackerInitialPosition,
                                destination=attackerDestinationPosition)
        goalBoardState = goalBoardState.resultantStateAfterAction(attackerAction)
        return goalBoardState

    def __normalMove(self, move, chessBoard, initialPosition, destinationPosition):
        """
        Takes a normal move and gets the goal board state from this normal move.
        Args:
            move: The move in uci form to be executed.
            chessBoard: A python chess board object.
            initialPosition: The initial position of the piece that is being moved.
            destinationPosition: The destination position of the piece that is being moved.
        """
        # Move the piece to its destination location.
        pieceInitialPosition = initialPosition
        pieceDestinationPosition = destinationPosition
        piece = self._boardState.getPieceAtLocation(pieceInitialPosition)
        action = Action(piece=piece, initialPosition=pieceInitialPosition, destination=pieceDestinationPosition)
        goalBoardState = self._boardState.resultantStateAfterAction(action)
        return goalBoardState

    def __findActionString(self, initialState, goalState):
        """
        Takes the initial and goal state and performs a best first search (in this case a greedy best first search) and
        then gets the actions the robotic assembly needs to take to reach that goal state.
        Args:
            initialState: The initial state (current state) of the board.
            goalState: The goal state of the board that we want to get to by performing actions with the robotic assembly.
        Returns:
            A string representing the actions to betaken by the robotic assembly.
        """
        # Construct the problem with the initial and the goal state.
        problem = Problem(initialState=initialState, goalState=goalState)
        # Perform the best first search and get the solution node.
        solutionNode = bestFirstSearch(problem)
        # Construct the solution handler that deals with the solution node and gets the actions required to get to the
        # goal board state as a string
        solutionHandler = SolutionHandler(solutionNode)
        # Get the action string
        return solutionHandler.getActionString()

    def gameEndMessage(self):
        """
        Does nothing at the minute. If desired could be repurposed to draw an image on the board with the pieces.
        """
        pass

    def resetBoard(self):
        """
        Resets the board state to its initial state.
        """
        # We need an intermediate state that is close to the final state and that can also get to the final state with
        # ease. I found that if I went straight to the intitial postion the gbfs would always hang I am fairly certain
        # this was because the pieces would get stuck in the middle behind a wall of pawns. The intermediate state
        # fixes this.
        resetStateDictionarySequence = [intermediateBoardEndStateDictionary, initialBoardStartStateDictionary]
        # Loop through the states getting the board to both states.
        for dictionary in resetStateDictionarySequence:
            goalState = BoardState(boardStateDictionary=dictionary)
            actionString = self.__findActionString(initialState=self._boardState, goalState=goalState)
            self._boardState = goalState
            self.__communicationManager.executeCommand(actionString, maxCommandSize=20)





