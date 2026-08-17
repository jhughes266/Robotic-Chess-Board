from dc_motor import DcMotor
from positional_encoder import PositionalEncoder
from pid_xy import PidXY
from servo_motor import ServoMotor
from time import sleep
from gripper import Gripper
from piece_mover import PieceMover
import random

mode = "NA"

# Testing Setup

# Setup the positional encoder
xBitPinNumberPairList = [0,1,2,3,4,5,6]
xPositionalEncoder = PositionalEncoder(bitPinNumberPairList=xBitPinNumberPairList)
yBitPinNumberPairList = [7,8,9,10,11,12,13]
yPositionalEncoder = PositionalEncoder(bitPinNumberPairList=yBitPinNumberPairList)

# Setup the motor objects
xDcMotor = DcMotor(speedControlPwmPinNumber=17, positivePinNumber=18, negativePinNumber=19)
yDcMotor = DcMotor(speedControlPwmPinNumber=14, positivePinNumber=15, negativePinNumber=16)

# Set up the PID
xMotorPidDict = {
    "Kp": 72,
    "Ki": 1,
    "Kd": 0
    }
yMotorPidDict = {
    "Kp": 72,
    "Ki": 1,
    "Kd": 0
    }

pid = PidXY(xPositionalEncoder=xPositionalEncoder,
                   yPositionalEncoder=yPositionalEncoder,
                   xDcMotor=xDcMotor,
                   yDcMotor=yDcMotor,
                   xMotorPidDict=xMotorPidDict,
                   yMotorPidDict=yMotorPidDict,
                   maxAllowableError=0)
# Set up the servo motors
vertical =  ServoMotor(angleControlPinNumber=20)
claw = ServoMotor(angleControlPinNumber=21)

# Set up the gripper
gripper = Gripper(verticalServo=vertical, clawServo=claw)

# Set up the piece mover
pieceMover = PieceMover(pidXY=pid, gripper=gripper)


if mode == "Positional Encoder":
    # Testing the Positional Encoder
    while True:
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
    
elif mode == "Motor":
    # Testing the Motor
    for i in range(2):
        testMotorX.turnMotor(100)
        sleep(1)
        testMotorX.turnMotor(-100)
        sleep(1)
        testMotorX.turnOff()

        testMotorY.turnMotor(100)
        sleep(1)
        testMotorY.turnMotor(-100)
        sleep(1)
        testMotorY.turnOff()
        
elif mode == "Motor and Positional Encoder":
    # Testing the positional encoder
    delay = 15
    print("X POSITIVE")
    testMotorX.turnMotor(100)
    for i in range(delay):
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
        sleep(0.05)

    print("X NEGATIVE")
    testMotorX.turnMotor(-100)
    for i in range(delay):
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
        sleep(0.05)

    testMotorX.turnOff()

    print("Y POSITIVE")
    testMotorY.turnMotor(100)
    for i in range(delay):
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
        sleep(0.05)


    print("Y NEGATIVE")
    testMotorY.turnMotor(100)
    for i in range(delay):
        xpos = xPositionalEncoder.getPosition()
        ypos = yPositionalEncoder.getPosition()
        print(f"Xpos {xpos}")
        print(f"Ypos {ypos}")
        sleep(0.05)

    testMotorY.turnOff()
        
elif mode == "Servo":
    # Testing the Servo
    for i in range(2):
        sleep(0.5)
        lower.angle(95)
        sleep(0.5)
        lower.angle(0)
        sleep(0.5)
        upper.angle(160)
        sleep(0.5)
        upper.angle(120)
        
    lower.angle(95)

elif mode == "PID":
    # Testing the PID
    for x in range(12,116,8):
        for y in range(12,116,8):
            testPid.moveTo(targetX=x, targetY=y)
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