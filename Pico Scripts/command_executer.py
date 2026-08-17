
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
    
    for character in command:
        
        if character == "B":
            pieceMover.
        elif character == "E":
            pass
            
