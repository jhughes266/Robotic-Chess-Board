import math

from piece_path_finding.problem import Problem
from piece_path_finding.problem import Problem
from piece_path_finding.priority_queue import PriorityQueue
from piece_path_finding.node import Node
from piece_path_finding.search_progress import SearchProgress
import math

def bestFirstSearch(problem):
    node = Node(state=problem.initialState, parent=None, action=None, pathCost=0, totalCost=math.inf, depth=0)
    frontier = PriorityQueue(sortingLambda=lambda node:node.totalCost)
    frontier.push(node)
    reached = {}
    reached[node.state.boardPosStringId()] = node.totalCost
    searchProgress = SearchProgress()
    while not frontier.empty():
        node = frontier.pop()

        searchProgress.updateProgress(node.totalCost)
        if problem.isGoal(node.state):
            return node

        for child in expand(problem, node):
            childState = child.state
            reachedId = childState.boardPosStringId()

            if (reachedId not in reached) or (child.totalCost < reached[reachedId]):
                reached[reachedId] = child.totalCost
                frontier.push(child)

    return None

def expand(problem, parentNode):
    childNodeList = []
    parentNodeState = parentNode.state

    for action in problem.actions(state=parentNodeState):
        childNodeState = problem.result(state=parentNodeState, action=action)
        gCost, hCost = problem.action_cost(oldState=parentNodeState, action=action, newState=childNodeState)
        childPathCost = parentNode.pathCost + gCost
        totalCost = hCost
        childNodeList.append(Node(state=childNodeState, parent=parentNode, action=action, pathCost=childPathCost, totalCost=totalCost, depth=parentNode.depth + 1))

    return childNodeList




