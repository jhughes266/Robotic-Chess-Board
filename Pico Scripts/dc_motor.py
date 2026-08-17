from machine import Pin
from machine import PWM

class DcMotor:
    """
    This class encapsulates the DC motor it enables the motor speed and direction
    of spin to be controlled.
    """
    def __init__(self, speedControlPwmPinNumber, positivePinNumber, negativePinNumber):
        """
        Sets up a "Motor" class object. Takes the pin number and inits "Pin"
        objects.
        Args:
            speedControlPWMPinNumber: The number of the pin responsible for pwm
            control of the motor.
            positivePinNumber: When this number pin is on and the negative pin
            is off the motor will go in the positive direction when activated.
            negativePinNumber: When this number pin is on and the positive pin
            is off the motor will go in the negative direction when activated.
        """
        self.__speedControlPwmPin = PWM(Pin(speedControlPwmPinNumber))
        self.__speedControlPwmPin.freq(1000) 
        self.__positivePin = Pin(positivePinNumber, Pin.OUT)
        self.__negativePin = Pin(negativePinNumber, Pin.OUT)
        # Make sure the motor is turned off
        self.turnOff()
    
    def __spinPositive(self):
        """
        Make the motor turn so the carriage will move in a positive dirrection
        """
        self.__negativePin.value(0)
        self.__positivePin.value(1)
    
    def __spinNegative(self):
        """
        Make the motor turn so the carriage will move in a negative dirrection
        """
        self.__positivePin.value(0)
        self.__negativePin.value(1)
    
    def turnMotor(self, percentageSpeed):
        """
        Activating this will cause the motor to spin at the given percentage of
        its maximum speed in the correct dirrection
        
        Args:
            percentageSpeed: The percentage of the maximum speed you want the
            motor spinning at takes values from 0-100 inclusive
        """
        # Determine the direction to spin the motor
        if percentageSpeed > 0:
            self.__spinPositive()
        elif percentageSpeed < 0:
            self.__spinNegative()
        else:
            self.turnOff()
            return
        
        #Output the PWM signal. Use the absolute value of the percentageSpeed
        self.__speedControlPwmPin.duty_u16(int(65535 * (abs(percentageSpeed) / 100)))
    
    def turnOff(self):
        """
        zeros everything causing the motor to halt
        """
        self.__negativePin.value(0)
        self.__positivePin.value(0)
        self.__speedControlPwmPin.duty_u16(0)
