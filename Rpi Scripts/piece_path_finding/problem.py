
class Problem:

    def __init__(self, initialState, goalState):
        self.initialState = initialState
        self.goalState = goalState

    def isGoal(self):
        return self.goalState == self.initialState

    def actions(self, state):
        return state.actions()

    def action_cost(self):
        pass

    def result(self, state, action):
        return state.resultantStateAfterAction(action)
