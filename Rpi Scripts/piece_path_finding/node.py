
class Node:
    """
    Node object that is used in the best first search algorithm.
    """
    def __init__(self, state, parent, action, pathCost, totalCost, depth):
        """
        Args:
            state: The state of the graph associated with the node.
            parent: The parent of this node. Once the goal is found the solution can trace back through its parents to get to the initial state and thus is finds a solution.
            action: The action that got us to the state on this node.
            pathCost: The CUMULATIVE path cost from the initial state to the current state.
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = pathCost
        self.totalCost = totalCost
        self.depth = depth