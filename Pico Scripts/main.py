from dc_motor import DcMotor
from positional_encoder import PositionalEncoder
from pid_xy import PidXY
from servo_motor import ServoMotor
from time import sleep
from gripper import Gripper
from piece_mover import PieceMover
import random

# 1 Testing the DcMotor object
"""
for i in range(2):
    testMotorX = DcMotor(speedControlPwmPinNumber=17, positivePinNumber=18, negativePinNumber=19)
    testMotorX.turnMotor(100)
    sleep(1)
    testMotorX.turnMotor(-100)
    sleep(1)
    testMotorX.turnOff()

    testMotorY = DcMotor(speedControlPwmPinNumber=14, positivePinNumber=15, negativePinNumber=16)
    testMotorY.turnMotor(100)
    sleep(1)
    testMotorY.turnMotor(-100)
    sleep(1)
    testMotorY.turnOff()
"""

# 2 Testing the positional encoder

xBitPinNumberPairList = [0,1,2,3,4,5,6]
xPositionalEncoder = PositionalEncoder(bitPinNumberPairList=xBitPinNumberPairList)
yBitPinNumberPairList = [7,8,9,10,11,12,13]
yPositionalEncoder = PositionalEncoder(bitPinNumberPairList=yBitPinNumberPairList)

testMotorX = DcMotor(speedControlPwmPinNumber=17, positivePinNumber=18, negativePinNumber=19)
testMotorY = DcMotor(speedControlPwmPinNumber=14, positivePinNumber=15, negativePinNumber=16)

delay = 15

"""
print("X POSITIVE")
testMotorX.turnMotor(100)
for i in range(delay):
    xpos = xPositionalEncoder.getPosition()
    ypos = yPositionalEncoder.getPosition()
    print("Xpos {}".format(xpos))
    print("Ypos {}".format(ypos))
    sleep(0.05)

print("X NEGATIVE")
testMotorX.turnMotor(-100)
for i in range(delay):
    xpos = xPositionalEncoder.getPosition()
    ypos = yPositionalEncoder.getPosition()
    print("Xpos {}".format(xpos))
    print("Ypos {}".format(ypos))
    sleep(0.05)

testMotorX.turnOff()

print("Y POSITIVE")
testMotorY.turnMotor(100)
for i in range(delay):
    xpos = xPositionalEncoder.getPosition()
    ypos = yPositionalEncoder.getPosition()
    print("Xpos {}".format(xpos))
    print("Ypos {}".format(ypos))
    sleep(0.05)


print("Y NEGATIVE")
testMotorY.turnMotor(100)
for i in range(delay):
    xpos = xPositionalEncoder.getPosition()
    ypos = yPositionalEncoder.getPosition()
    print("Xpos {}".format(xpos))
    print("Ypos {}".format(ypos))
    sleep(0.05)

testMotorY.turnOff()


#testMotorY.turnMotor(-100)
while True:
    xpos = xPositionalEncoder.getPosition()
    ypos = yPositionalEncoder.getPosition()
    print("Xpos {}".format(xpos))
    print("Ypos {}".format(ypos))
    sleep(0.1)

#testMotorY.turnOff()

    

"""
# 3 Testing the pid
def repos(sleepTime):
    xBitPinNumberPairList = [0,1,2,3,4,5,6]
    xPositionalEncoder = PositionalEncoder(bitPinNumberPairList=xBitPinNumberPairList)
    yBitPinNumberPairList = [7,8,9,10,11,12,13]
    yPositionalEncoder = PositionalEncoder(bitPinNumberPairList=yBitPinNumberPairList)

    testMotorX = DcMotor(speedControlPwmPinNumber=17, positivePinNumber=18, negativePinNumber=19)
    testMotorY = DcMotor(speedControlPwmPinNumber=14, positivePinNumber=15, negativePinNumber=16)

    #testMotorX.turnMotor(-100)
    #sleep(sleepTime)
    #testMotorX.turnOff()

    testMotorY.turnMotor(-100)
    sleep(sleepTime)
    testMotorY.turnOff()
    
reposition = False;

if reposition:
    repos(0.25)
    
else:
    
    xBitPinNumberPairList = [0,1,2,3,4,5,6]
    xPositionalEncoder = PositionalEncoder(bitPinNumberPairList=xBitPinNumberPairList)
    yBitPinNumberPairList = [7,8,9,10,11,12,13]
    yPositionalEncoder = PositionalEncoder(bitPinNumberPairList=yBitPinNumberPairList)

    xDcMotor = DcMotor(speedControlPwmPinNumber=17, positivePinNumber=18, negativePinNumber=19)
    yDcMotor = DcMotor(speedControlPwmPinNumber=14, positivePinNumber=15, negativePinNumber=16)
    
    xDcMotor.turnOff()
    yDcMotor.turnOff()
    
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

    testPid = PidXY(xPositionalEncoder=xPositionalEncoder,
                       yPositionalEncoder=yPositionalEncoder,
                       xDcMotor=xDcMotor,
                       yDcMotor=yDcMotor,
                       xMotorPidDict=xMotorPidDict,
                       yMotorPidDict=yMotorPidDict,
                       maxAllowableError=0)
    """
    for x in range(12,116,8):
        for y in range(12,116,8):
            testPid.moveTo(targetX=x, targetY=y)
            print("Xpos" + str(xPositionalEncoder.getPosition()))
            print("Ypos" + str(yPositionalEncoder.getPosition()))
            print("AT Target")

    
    
    for i in range(2):
        
        testPid.moveTo(targetX=10, targetY=10)
        print("Xpos" + str(xPositionalEncoder.getPosition()))
        print("Ypos" + str(yPositionalEncoder.getPosition()))
        print("AT Target")
        
        testPid.moveTo(targetX=10, targetY=110)
        print("Xpos" + str(xPositionalEncoder.getPosition()))
        print("Ypos" + str(yPositionalEncoder.getPosition()))
        print("AT Target")
        
        testPid.moveTo(targetX=110, targetY=110)
        print("Xpos" + str(xPositionalEncoder.getPosition()))
        print("Ypos" + str(yPositionalEncoder.getPosition()))
        print("AT Target")
        
        testPid.moveTo(targetX=110, targetY=10)
        print("Xpos" + str(xPositionalEncoder.getPosition()))
        print("Ypos" + str(yPositionalEncoder.getPosition()))
        print("AT Target")
        
        testPid.moveTo(targetX=10, targetY=10)
        print("Xpos" + str(xPositionalEncoder.getPosition()))
        print("Ypos" + str(yPositionalEncoder.getPosition()))
        print("AT Target")
        
        testPid.moveTo(targetX=55, targetY=110)
        print("Xpos" + str(xPositionalEncoder.getPosition()))
        print("Ypos" + str(yPositionalEncoder.getPosition()))
        print("AT Target")
        
        testPid.moveTo(targetX=110, targetY=10)
        print("Xpos" + str(xPositionalEncoder.getPosition()))
        print("Ypos" + str(yPositionalEncoder.getPosition()))
        print("AT Target")
        
        testPid.moveTo(targetX=55, targetY=55)
        print("Xpos" + str(xPositionalEncoder.getPosition()))
        print("Ypos" + str(yPositionalEncoder.getPosition()))
        print("AT Target")
        
        testPid.moveTo(targetX=10, targetY=10)
        print("Xpos" + str(xPositionalEncoder.getPosition()))
        print("Ypos" + str(yPositionalEncoder.getPosition()))
        print("AT Target")
        """
    #testPid.moveTo(targetX=55, targetY=55)
    #testPid.moveTo(targetX=11, targetY=10)
    
    vertical =  ServoMotor(angleControlPinNumber=20)
    claw = ServoMotor(angleControlPinNumber=21)
    """
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
    """
    gripper = Gripper(verticalServo=vertical, clawServo=claw)
    #gripper.disengage()
    #gripper.engage()
    
    #testPid.moveTo(targetX=11, targetY=11)
    #testPid.moveTo(targetX=55, targetY=55)
    
    #gripper.disengage()
    
    pieceMover = PieceMover(pidXY=testPid, gripper=gripper)
    #pieceMover.movePiece(startGridX=0, startGridY=0, endGridX=5, endGridY=7, engageGripper=False, disengageGripper=False)
    #pieceMover.moveToCalibration()
    #pieceMover.moveToGridXY(0,0)
    #pieceMover.moveToCalibration()
    
    #for x in range(12):
    #    for y in range(12):
    #            pieceMover.movePiece(startGridX=x, startGridY=y, endGridX=x, endGridY=y, engageGripper=False, disengageGripper=False)
    """
    startX = 0
    startY = 0
    for i in range(30):
        endX = random.randint(0,11)
        endY = random.randint(0,11)
        pieceMover.movePiece(startGridX=startX, startGridY=startY, endGridX=endX, endGridY=endY, engageGripper=True, disengageGripper=True)
        startX = endX
        startY = endY
    
    pieceMover.movePiece(startGridX=startX, startGridY=startY, endGridX=0, endGridY=0, engageGripper=True, disengageGripper=True)

    """
    pieceMover.movePiece(startGridX=1, startGridY=1, endGridX=3, endGridY=1, engageGripper=True, disengageGripper=True)
    pieceMover.movePiece(startGridX=3, startGridY=1, endGridX=3, endGridY=5, engageGripper=True, disengageGripper=True)
    pieceMover.movePiece(startGridX=3, startGridY=5, endGridX=1, endGridY=5, engageGripper=True, disengageGripper=True)
    pieceMover.movePiece(startGridX=1, startGridY=5, endGridX=3, endGridY=5, engageGripper=True, disengageGripper=True)
    pieceMover.movePiece(startGridX=3, startGridY=5, endGridX=3, endGridY=1, engageGripper=True, disengageGripper=True)
    pieceMover.movePiece(startGridX=3, startGridY=1, endGridX=1, endGridY=1, engageGripper=True, disengageGripper=True)













        
    

    

        
        
        


