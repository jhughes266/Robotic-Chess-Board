from time import sleep
from dc_motor import DcMotor

from robot_object_config import xPositionalEncoder, yPositionalEncoder, xDcMotor, yDcMotor, pid, vertical, claw, gripper, pieceMover

mode = "NA"


if mode == "Positional Encoder":
    # Testing the Positional Encoder
    while True:
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
    
elif mode == "Motor":
    # Testing the Motor
    for i in range(1):
        xDcMotor.turnMotor(100)
        sleep(1)
        xDcMotor.turnMotor(-100)
        sleep(1)
        xDcMotor.turnOff()

        yDcMotor.turnMotor(100)
        sleep(1)
        yDcMotor.turnMotor(-100)
        sleep(1)
        yDcMotor.turnOff()
        
elif mode == "Motor and Positional Encoder":
    # Testing the positional encoder
    delay = 15
    print("X POSITIVE")
    xDcMotor.turnMotor(100)
    for i in range(delay):
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
        sleep(0.05)

    print("X NEGATIVE")
    xDcMotor.turnMotor(-100)
    for i in range(delay):
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
        sleep(0.05)

    xDcMotor.turnOff()

    print("Y POSITIVE")
    yDcMotor.turnMotor(100)
    for i in range(delay):
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
        sleep(0.05)


    print("Y NEGATIVE")
    yDcMotor.turnMotor(-100)
    for i in range(delay):
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
        sleep(0.05)

    yDcMotor.turnOff()
        
elif mode == "Servo":
    # Testing the Servo
    
    sleep(0.5)
    vertical.angle(0)
    sleep(0.5)
    claw.angle(120)
    sleep(3)
        
    claw.angle(160)
    sleep(0.5)
    vertical.angle(95)
    sleep(0.5)


elif mode == "PID":
    # Testing the PID
    for x in range(12,116,8):
        for y in range(12,116,8):
            pid.moveTo(targetX=x, targetY=y)
            print("Xpos" + str(xPositionalEncoder.getPosition()))
            print("Ypos" + str(yPositionalEncoder.getPosition()))
            print("AT Target")

elif mode == "Gripper":
    # Testing the gripper
    gripper.disengage()
    gripper.engage()
    gripper.disengage()
    
    
    
elif mode == "Piece Mover":
    # Testing the piece mover
    pieceMover.moveToCalibration()
    pieceMover.moveToGridXY(gridX=0, gridY=0)
    pieceMover.engageGripper()
    pieceMover.moveToGridXY(gridX=1, gridY=0)
    pieceMover.moveToGridXY(gridX=0, gridY=0)
    pieceMover.disengageGripper()

print("End of Test!")