
class Problem:

    def __init__(self, initialState, goalState):
        self.initialState = initialState
        self.goalState = goalState

    def isGoal(self, state):
        return self.goalState == state

    def actions(self, state):
        return state.actions()

    def action_cost(self, oldState, action, newState):
        gCost = 1
        hCost = newState.distanceToL2(self.goalState)
        return gCost, hCost

    def result(self, state, action):
        return state.resultantStateAfterAction(action)
