import copy

from piece_path_finding import action


class SolutionHandler:
    """
    This class is responsible for handling the solution node.
    """
    def __init__(self, solutionNode):
        """
        Initializes the SolutionHandler class.
        Args:
            solutionNode: SolutionNode object that contains a solution to the search problem.
        """
        self.__solutionList = self.__constructSolutionList(solutionNode)

    def __constructSolutionList(self, solutionNode):
        """
        Develops a list that contains all the nodes in order that lead to a solution.
        Args:
             solutionNode: SolutionNode object that contains a solution to the search problem.
        Returns:
            solutionList: A list that contains all the nodes in order that lead to a solution.
        """
        node = solutionNode
        solutionList = []
        # We dont need the root node because it contains no additional information.
        while node.parent is not None:
            solutionList.append(node)
            node = node.parent
        # Reverse the list. So that the zeroth element is the zeroth step.
        solutionList.reverse()
        return solutionList

    def __isActionDirectionChange(self, previousAction, currentAction):
        """
        Determines if current action causes a direction change.
        Args:
             previousAction: Contains the previous action object
             currentAction: Contains the current action object
        Returns:
            A boolean that indicates if there has been a direction change.
        """
        # The previous actions initial position.
        previousX = previousAction.initialPosition[0]
        previousY = previousAction.initialPosition[1]
        # The next actions initial position.
        nextX = currentAction.destination[0]
        nextY = currentAction.destination[1]
        # There has been a direction change only when both coordinates differ. It only works for 90 degree changes not 180
        # degree changes. This doesn't matter because for a given movement the piece won't backtrack because this would
        # represent a repeated state which is impossible due to the search algorithm.
        return ((previousX != nextX) and (previousY != nextY))

    def retrieveNeccesaryActions(self):
        """
        Trims down the actions by removing unnecessary actions that are just straight between two points. This is probably
        not the most efficient implementation but compared to the search it will be negligible.
        Returns:
            trimmedJaggeredList: A nested jaggered list. Each element is a list that contains a group of actions for a piece.
            The piece can appear multiple times in the list. The list is in chronological order of movements (this means
            one piece can be moved, then another "x" pieces, then the original piece.) This output data structure will
            be easy to use when moving pieces. At the start of each action grouping The gripper will be engaged all the
            movements performed. It will then be disengaged and moved to the next piece and re-engaged and so on.
        """
        # Creating action list
        actionList = []
        for node in self.__solutionList:
            actionList.append(node.action)

        # Grouping actions by piece (in chronological order each new nested list means the piece being moved has changed)
        jaggeredActionList = [[]]
        j = 0
        # Get the first action
        currentAction = actionList[0]
        # Append the first action inside the first grouping for the jaggeredActionList
        jaggeredActionList[j].append(currentAction)
        # Loop through all the actions (we already have the first this is necessary as we are looking backwards)
        for i in range(1, len(actionList)):
            # Get the current and previous actions.
            previousAction = actionList[i-1]
            currentAction = actionList[i]
            # If the pieces don't match we want another grouping in the jaggered action list. This corresponds to another
            # set of actions for a given piece (this isn't necessarily all the actions for a given we have just
            # transitioned to another piece.)
            if previousAction.piece != currentAction.piece:
                # Add another nested list.
                jaggeredActionList.append([])
                # Increase j so we are targeting the new nested list.
                j += 1
            # Add the current action
            jaggeredActionList[j].append(currentAction)

        # Removing straight line actions (except start and end actions).
        # A new list that is a trimmed down version of the original.
        trimmedJaggeredActionList = []
        # Loop through all the action groupings (which are grouped by piece).
        for i, pieceActionGroup in enumerate(jaggeredActionList):
            # Add another entry for a new grouping.
            trimmedJaggeredActionList.append([])
            # Add the first action to a given grouping because we will be looking back in the next for loop.
            trimmedJaggeredActionList[i].append(pieceActionGroup[0])
            # Loop through all the actions in the specified grouping. Except the first and the last. The first has already
            # been added and the last has to be added. If this wasn't done there is a chance the last could be deemed
            # straight and not be added which would mean that the piece wouldn't end up in the desired location. This
            # does mean that sometimes though the final action is straight. This is delt with later on in this function.
            for j in range(1, len(pieceActionGroup)-1):
                # Getting the current and the previous action.
                previousAction = pieceActionGroup[j-1]
                currentAction = pieceActionGroup[j]
                # Checking if a direction change has taken place. We only add actions that change the direction. The rest
                # of the actions are straight and are uneeded.
                if self.__isActionDirectionChange(previousAction=previousAction, currentAction=currentAction):
                    trimmedJaggeredActionList[i].append(currentAction)
            # Before adding the final action to the grouping the list has to be greater than 1 length. Otherwise on
            # single action groupings we would get a repeat.
            if len(pieceActionGroup) > 1:
                trimmedJaggeredActionList[i].append(pieceActionGroup[-1])


        # This portion of the function link the actions by setting the previous actions destination to the current actions
        # initial position. This is required because straight actions have been removed. We are essentially linking up the
        # straight actions.
        for pieceActionGroup in trimmedJaggeredActionList:
            for i in range(1, len(pieceActionGroup)):
                previousAction = pieceActionGroup[i-1]
                currentAction = pieceActionGroup[i]
                previousAction.destination = currentAction.initialPosition


        # The last action has the potential to be part of a straight due to the way the original list was constructed. The final action had
        # to be included otherwise if was considered straight it would have been neglected which is not acceptable. This
        # meant it had to be added to the list. In the part below we check if the final action is straight and if it is
        # we update the preceding action then remove the final one.
        for pieceActionGroup in trimmedJaggeredActionList:
            # This is only relevant for groupings with more than 2 actions.
            if len(pieceActionGroup) < 2:
                continue
            # Get the final and the second final action
            finalAction = pieceActionGroup[-1]
            secondFinalAction = pieceActionGroup[-2]

            # If the two above actions are not part of a direction change (ie: are straight) we update the second final
            # action to make its destination the final actions destination. We then remove the final action.
            if not self.__isActionDirectionChange(previousAction=secondFinalAction, currentAction=finalAction):
                secondFinalAction.destination = finalAction.destination
                pieceActionGroup.pop(-1)

        return trimmedJaggeredActionList



    def __str__(self):
        """
        Returns the string representation of the solution.
        Returns:
             outputString: A string representation of the solution.
        """
        outputString = "\nSOLUTION START ##############################\n"
        for i, node in enumerate(self.__solutionList):
            outputString += "Action number: " + str(i + 1) + "\n"
            outputString += str(node.action) + "\n"
            outputString += str(node.state) + "\n"
            outputString += "-------------------------------\n"
        outputString += "SOLUTION END ##############################\n"
        return outputString
