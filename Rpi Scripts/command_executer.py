def excuteCommand(command, pieceMover, mode="real"):
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
    Returns:

    """
    # The mode is fake so we just bypass the function.
    if mode == "fake":
        print("Mode is fake. This message is to signify a mock moving of the pieces. Returning from function!")
        return

    # First we disengage the gripper to make sure it wont interfer with any pieces
    pieceMover.disengageGripper()

    i = 0
    while i < len(command):

        character = command[i]
        gridX, gridY = None, None

        if character == "[":
            j = i
            posStr = ""
            while True:
                j += 1
                if command[j] == ",":
                    gridX = int(posStr)
                    posStr = ""
                    continue
                elif command[j] == "]":
                    gridY = int(posStr)
                    break
                posStr += command[j]

            pieceMover.moveToGridXY(gridX, gridY)
        elif character == "E":
            pieceMover.engageGripper()
        elif character == "D":
            pieceMover.disengageGripper()

        i += 1




class PieceMover:
    def engageGripper(self):
        print("Engaging Gripper")

    def disengageGripper(self):
        print("Disengaging Gripper")

    def moveToGridXY(self, gridX, gridY):
        print(f"Moving to X:{gridX}, Y:{gridY}")

testCommand = "[8,3]E[10,4]D[8,2]E[8,3]D[8,4]E[9,4]D[8,3]E[8,4][7,4]D[9,4]E[8,4][8,3]D"
excuteCommand(testCommand, pieceMover=PieceMover())


