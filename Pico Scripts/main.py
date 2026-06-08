from dc_motoro import DcMotor
from positional_encoder import PositionalEncoder
from pid_xy import PidXY
from time import sleep

# 1 Testing the DcMotor object
testMotor = DcMotor(speedControlPwmPinNumber=14, positivePinNumber=15, negativePinNumber=16)
testMotor.turnMotor(100)
sleep(3.0)
testMotor.turnMotor(-100)
sleep(3.0)
testMotor.turnOff()

# 2 Testing the positional encoder
xBitPinPairList = [0,1,2,3,4,5,6]
xPositionalEncoder = PositionalEncoder(bitPinNumberPairList=xBitPinNumberPairList)
yBitPinPairList = [7,8,9,10,11,12,13]
yPositionalEncoder = PositionalEncoder(bitPinNumberPairList=yBitPinNumberPairList)
print(xPositionalEncoder.getPosition())
print(yPositionalEncoder.getPosition())

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


