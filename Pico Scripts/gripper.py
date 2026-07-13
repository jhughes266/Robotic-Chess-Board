from servo_motor import ServoMotor
from time import sleep

class Gripper:
    
    def __init__(self, verticalServo, clawServo):
        """
        Controls the gripper that is responsible for gripping chess pieces.
        Args:
            verticalServo: The servo object to control the vertical servo.
            clawServo: The servo object to control the claw servo.
        """
        self._verticalServo = verticalServo
        self._clawServo = clawServo
        self._verticalStartAngle = 95
        self._verticalEndAngle = 20
        self._clawStartAngle = 141
        self._clawEndAngle = 120
        # Disengage the servo at first.
        self.disengage()
    
    def engage(self):
        """
        Engages the gripper so it is ready to hold a piece.
        """
        # First move the vertical servo up
        self._verticalServo.angle(self._verticalEndAngle)
        # Sleep (this may need tuning) to ensure that the vertical servo is
        # at its final position.
        time.sleep(0.75)
        self._clawServo.angle(self._clawEndAngle)

    def disengage(self):
        """
        Disenages teh gripper so that it realeases the piece.
        """
        # Open the claw.
        self._clawServo.angle(self._clawStartAngle)
        # Wait a tiny amount of time (may need adjusting) just so that when the
        # vertical servo moves down it doesnt potentially intefer with the
        # magnet.
        time.sleep(0.1)
        # Move the vertical servo to its start postion
        self._verticalServo.angle(self._verticalStartAngle)
        # Turn both servos off the claw servo may need to remain on.
        self._clawServo.turnOff()
        self._verticalServo.turnOff()
        

        