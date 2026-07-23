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
        self.__verticalServo = verticalServo
        self.__clawServo = clawServo
        self.__verticalStartAngle = 95
        self.__verticalEndAngle = 0
        self.__clawStartAngle = 130
        self.__clawEndAngle = 120
        # Disengage the servo at first.
        self.disengage()
    
    def engage(self):
        """
        Engages the gripper so it is ready to hold a piece.
        """
        # First move the vertical servo up
        self.__verticalServo.angle(self.__verticalEndAngle)
        # Sleep (this may need tuning) to ensure that the vertical servo is
        # at its final position.
        sleep(0.5)
        self.__clawServo.angle(self.__clawEndAngle)

    def disengage(self):
        """
        Disenages teh gripper so that it realeases the piece.
        """
        # Open the claw.
        self.__clawServo.angle(self.__clawStartAngle)
        # Wait a tiny amount of time (may need adjusting) just so that when the
        # vertical servo moves down it doesnt potentially intefer with the
        # magnet.
        sleep(0.5)
        # Move the vertical servo to its start postion
        self.__verticalServo.angle(self.__verticalStartAngle)
        # Pause so motor has time to go to angle
        sleep(0.5)
        # Turn both servos off the claw servo may need to remain on.
        self.__clawServo.turnOff()
        self.__verticalServo.turnOff()
        

        