from robot_object_config import pieceMover
from command_executer import excuteCommand
import random

# Make the number of itterations 40
def magnet_tester(numberOfIterations):
    """
    This function is designed to test how well different magnets and materials
    on the board perform. It randomly moves a single magnet over the board to
    different locations.
    Args:
        numberOfIterations: The number of testing itterations
    """
    # Where the magnet intially starts
    initialMagnetLocation = [0,0]
    # The current location of the magnet
    currentMangetLocation = initialMagnetLocation[::]
    # Disengage the gripper before the program starts
    pieceMover.disengageGripper()
    # Loop through the specified number of itterations
    for iteration in range(1, numberOfIterations):
        # Move to the current location and engage the gripper
        pieceMover.moveToGridXY(gridX=currentMagnetLocation[0], gridY=currentMagnetLocation[1])
        pieceMover.engageGripper()
        # Get a new location and move the magner there and then disengage the
        # gripper.
        newX = random.randint(0,11)
        newy = random.randint(0,11)
        pieceMover.moveToGridXY(gridX=newX, gridY=newY)
        pieceMover.disengageGripper()
        # Update the current location of the magnet
        currentMagnetLocation[0] = newX
        currentMagnetLocation[1] = newY
        # This pauses the execution of the routine incase a magnet has fallen
        haltFlag = input("Enter nothing to continue OR enter anything to halt")
        
        
    # Move the magnet back to the starting location
    pieceMover.moveToGridXY(gridX=currentMagnetLocation[0], gridY=currentMagnetLocation[1])
    pieceMover.engageGripper()
    
    pieceMover.moveToGridXY(gridX=initialMagnetLocation[0], gridY=initialMagnetLocation[1])
    pieceMover.disengageGripper()
    print("Program end!!!")

