
def excuteCommand(command, pieceMover, mode="real", baseOffset=2):
    """
    This function takes a command in string form that is read and then excuted by
    the pico causing the robotic assembly to move.
    Args:
        command: A string that contains the commands for the robot and will parsed
        and have the commands extracted and exectued.
        pieceMover: A piece mover object that allows the function to move the
        robotic assembly.
        mode: The mode can be "fake" or "real". Fake is for when the robot is not connected
        it allows the pico to send messages mimicing that it has moved to the correct
        location. Real will move the robotic assembly.
        baseOffset:A offset in the base coordinate system that is added
        to the base position retrieved from the dictionary that maps between
        the base and grid coordinate systems. This has been added due to the
        strength of the magnets being used which mean the piece is dragged
        behind the carriage when it moves. The offset allows correction of
        this.
    Returns:

    """
    # The mode is fake so we just bypass the function.
    if mode == "fake":
        print("Mode is fake. This message is to signify a mock moving of the pieces. Returning from function!")
        return

    # First we disengage the gripper to make sure it wont interfer with any pieces
    #pieceMover.disengageGripper()
    print(command)
    print(len(command))
    
    # Initiating all the grid and previous grid positions with Nones
    gridX, gridY, prevGridX, prevGridY = None, None, None, None
    # Initiating the posStr to an empty string. This string is responsible for storing the postions within the
    # commands.
    posStr = ""
    for i in range(len(command)):
        # Extract the character from the given command
        character = command[i]
        # An open square bracket indicates the start of a position to be moved to
        if character == "[":
            # Stores the position of the command.
            posStr = ""
            # Continue so that the '[' is not added to the posStr var
            continue
        # The ',' indicates that the X grid position has been found.
        elif character == ",":
            gridX = int(posStr)
            posStr = ""
            # Continue so that the ',' is not added to the posStr var
            continue
        # The ']' indicates that the Y grid position has been found.
        elif character == "]":
            gridY = int(posStr)
            # The offsets both start as 0 and then are altered below if required.
            xbaseOffset, ybaseOffset = 0, 0
            # We only calculate the respective base offsets when the
            # previous grid positions have been calculated
            if prevGridX is not None and prevGridY is not None:
                difX = gridX - prevGridX
                difY = gridY - prevGridY
                # The offsets are in the direction of movement as the piece is being
                # dragged behind so we calculate the sign of the movement of direction
                # and then multiply it by the baseoffset
                if difX != 0:
                    xbaseOffset = (difX/abs(difX)) * baseOffset
                    
                if difY != 0:
                    ybaseOffset = (difY/abs(difY)) * baseOffset
            # Move the pieces to the grid location taking the base offsets
            # into account.
            print(f"Moving to gridX: {gridX}, gridY: {gridY}, xbaseOffset: {xbaseOffset}, ybaseOffset: {ybaseOffset}")
            pieceMover.moveToGridXY(gridX, gridY, xbaseOffset, ybaseOffset)
            # Update the previous grid locations
            prevGridX = gridX
            prevGridY = gridY
        # Engage the gripper
        elif character == "E":
            pieceMover.engageGripper()
        # Disengage the gripper
        elif character == "D":
            pieceMover.disengageGripper()
            # When the gripper is disengaged we know the next move wont be
            # carrying a piece it will be simply moving to a location ready to
            # pick up the next piece we therefore dont want any offset during
            # this move.
            prevGridX, prevGridY = None, None
        
        posStr += character
    
        


