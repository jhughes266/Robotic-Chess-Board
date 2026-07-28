import math

from piece_path_finding.problem import Problem
from piece_path_finding.problem import Problem
from piece_path_finding.priority_queue import PriorityQueue
from piece_path_finding.node import Node
from piece_path_finding.search_progress import SearchProgress
import math

def bestFirstSearch(problem):
    """
    Performs the best-first search algorithm.
    Args:
         problem: The search problem to be solved.
    Returns:
        node: A node that is linked to its parents and can be used to obtain the solution.
    """
    # Get the initial node with the initial problem state.
    node = Node(state=problem.initialState, parent=None, action=None, pathCost=0, totalCost=math.inf, depth=0)
    # A frontier that sorts its collection by the total cost of the node.
    frontier = PriorityQueue(sortingLambda=lambda node:node.totalCost)
    # Push the node onto the frontier.
    frontier.push(node)
    # A dictionary that stores all the reached board positions
    reached = {}
    # Add the initial state as an entry.
    reached[node.state.boardPosStringId()] = node.totalCost
    # A search progress object used to track how the search is progressing
    searchProgress = SearchProgress()
    # Keep looping through until all nodes have been removed from the frontier. To be fair this may as well be while
    # true exploring the entire state space for this problem is intractable.
    while not frontier.empty():
        # Pop the lowest cost node off the priority queue.
        node = frontier.pop()
        # Update the search progress.
        searchProgress.updateProgress(node.totalCost)
        # Check if the popped node is the goal. If it is return it as we have found the solution
        if problem.isGoal(node.state):
            return node
        # Expand the popped node to further explore the state space graph
        for child in expand(problem, node):
            childState = child.state
            # Get the id of the child state that will be used in the reached dictionary.
            reachedId = childState.boardPosStringId()
            # If the board state has not been reached or the total cost to get to the child is less than the entry then
            # update the reached dictionary and push the child onto the priority queue as we want to explore it further
            if (reachedId not in reached) or (child.totalCost < reached[reachedId]):
                reached[reachedId] = child.totalCost
                frontier.push(child)
    #No solution was found
    return None

def expand(problem, parentNode):
    """
    Expands the parent node and returns a list of all child nodes that contain all the actions available from the parent
    node.
    Args:
        problem: The search problem.
        parentNode: The node who's children we want to find.
    """
    childNodeList = []
    parentNodeState = parentNode.state

    # Loop through all the available actions in the parent nodes state.
    for action in problem.actions(state=parentNodeState):
        # Get the new child node state
        childNodeState = problem.result(state=parentNodeState, action=action)
        # Get the g and the hcost of the action
        gCost, hCost = problem.action_cost(oldState=parentNodeState, action=action, newState=childNodeState)
        # Update the childs path cost
        childPathCost = parentNode.pathCost + gCost
        # We are using greedy best first search (just the hcost) otherwise the problem takes far to long to solve if
        # using A star
        totalCost = hCost
        # Append a new child node to the child node list
        childNodeList.append(Node(state=childNodeState, parent=parentNode, action=action, pathCost=childPathCost, totalCost=totalCost, depth=parentNode.depth + 1))

    return childNodeList




