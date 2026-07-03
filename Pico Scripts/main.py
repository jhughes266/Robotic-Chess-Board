from dc_motor import DcMotor
from positional_encoder import PositionalEncoder
#from pid_xy import PidXY
from time import sleep

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

delay = 20

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
testMotorY.turnMotor(-100)
for i in range(delay):
    xpos = xPositionalEncoder.getPosition()
    ypos = yPositionalEncoder.getPosition()
    print("Xpos {}".format(xpos))
    print("Ypos {}".format(ypos))
    sleep(0.05)

testMotorY.turnOff()


    
"""
# 3 Testing the pid
xBitPinPairList = [0,1,2,3,4,5,6]
xPositionalEncoder = PositionalEncoder(bitPinNumberPairList=xBitPinNumberPairList)
yBitPinPairList = [7,8,9,10,11,12,13]
yPositionalEncoder = PositionalEncoder(bitPinNumberPairList=yBitPinNumberPairList)
xDcMotor = DcMotor(speedControlPwmPinNumber=14, positivePinNumber=15, negativePinNumber=16)
yDcMotor = DcMotor(speedControlPwmPinNumber=17, positivePinNumber=18, negativePinNumber=19)
xMotorPidDict = {
    "Kp": 1,
    "Ki": 1,
    "Kd": 1
    }
yMotorPidDict = {
    "Kp": 1,
    "Ki": 1,
    "Kd": 1
    }

testPid = PidXY(xPositionalEncoder=xPositionalEncoder,
                   yPositionalEncoder=yPositionalEncoder,
                   xDcMotor=xDcMotor,
                   yDcMotor=yDcMotor,
                   xMotorPidDict=xMotorPidDict,
                   yMotorPidDict=yMotorPidDict,
                   maxAllowableError=1)

testPid.moveTo(xTarget=, yTarget=)
"""

