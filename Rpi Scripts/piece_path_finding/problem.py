
class Problem:
    """
    Encapsulate the problem class that is used in the best first search algorithm.
    """
    def __init__(self, initialState, goalState):
        """
        Initialize the problem class
        Args:
             initialState: The initial state for the problem which is a board state object.
             goalState: The goal state for the problem which is a goal state object.
        """
        self.initialState = initialState
        self.goalState = goalState

    def isGoal(self, state):
        """
        Determine if the state is goal or not.
        Args:
            state: The state that we want to check against the goal state of the problem.
        Returns:
            A bool indicating if the state is goal or not.
        """
        return self.goalState == state

    def actions(self, state):
        """
        Returns a list of the actions available in the provided state.
        Args:
            state: The state whos available actions we want to find.
        Returns:
            A list of the actions available in the provided state.
        """
        return state.actions()

    def action_cost(self, oldState, action, newState):
        """
        Returns the cost of performing an action of moving from the old state to the new state.
        Args:
            oldState: The state before the action.
            action: The action to perform on the old state.
            newState: The state after the action.
        Returns:
            gCost: The cost of performing the given action.
            hCost: The estimate cost to the goal state.
        """
        # All actions have exactly the same cost.
        gCost = 1
        # The heuristic used is the Euclidean distance.
        hCost = newState.distanceToL2(self.goalState)
        return gCost, hCost

    def result(self, state, action):
        """
        Returns a new BoardState object that results after applying the argument action to the argument state.
        Args:
            state: The state to apply the action to.
            action: The action that is to be applied to the state.
        Returns:
            A new state that results from applying the action on the state.
        """
        return state.resultantStateAfterAction(action)
