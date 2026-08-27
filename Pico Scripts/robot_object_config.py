from dc_motor import DcMotor
from positional_encoder import PositionalEncoder
from pid_xy import PidXY
from servo_motor import ServoMotor
from gripper import Gripper
from piece_mover import PieceMover

# Setup the positional encoder
xBitPinNumberPairList = [0,1,2,3,4,5,6]
xPositionalEncoder = PositionalEncoder(bitPinNumberPairList=xBitPinNumberPairList)
yBitPinNumberPairList = [7,8,9,10,11,12,13]
yPositionalEncoder = PositionalEncoder(bitPinNumberPairList=yBitPinNumberPairList)

# Setup the motor objects
xDcMotor = DcMotor(speedControlPwmPinNumber=17, positivePinNumber=19, negativePinNumber=18)
yDcMotor = DcMotor(speedControlPwmPinNumber=14, positivePinNumber=15, negativePinNumber=16)

# Set up the PID
xMotorPidDict = {
    "Kp": 72,
    "Ki": 3,
    "Kd": 0
    }
yMotorPidDict = {
    "Kp": 72,
    "Ki": 3,
    "Kd": 0
    }

pid = PidXY(xPositionalEncoder=xPositionalEncoder,
                   yPositionalEncoder=yPositionalEncoder,
                   xDcMotor=xDcMotor,
                   yDcMotor=yDcMotor,
                   xMotorPidDict=xMotorPidDict,
                   yMotorPidDict=yMotorPidDict,
                   maxAllowableError=1)
# Set up the servo motors
vertical =  ServoMotor(angleControlPinNumber=26)
claw = ServoMotor(angleControlPinNumber=22)

# Set up the gripper
gripper = Gripper(verticalServo=vertical, clawServo=claw)

# Set up the piece mover
pieceMover = PieceMover(pidXY=pid, gripper=gripper)