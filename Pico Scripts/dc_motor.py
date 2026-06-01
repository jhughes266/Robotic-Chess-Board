from machine import Pin

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
        self._speedControlPwmPin = PWM(Pin(speedControlPwmPinNumber))
        self._speedControlPwmPin.freq(1000) 
        self._positivePin = Pin(positivePinNumber, Pin.OUT)
        self._negativePin = Pin(negativePinNumber, Pin.OUT)
    
    def _spinPositive():
        """
        Make the motor turn so the carriage will move in a positive dirrection
        """
        self._negative.value(0)
        self._positive.value(1)
    
    def _spinNegative():
        """
        Make the motor turn so the carriage will move in a negative dirrection
        """
        self._positive.value(0)
        self._negative.value(1)
    
    def turnMotor(percentageSpeed):
        """
        Activating this will cause the motor to spin at the given percentage of
        its maximum speed in the correct dirrection
        
        Args:
            percentageSpeed: The percentage of the maximum speed you want the
            motor spinning at takes values from 0-100 inclusive
        """
        # Determine the direction to spin the motor
        if percentageSpeed > 0:
            self._spinPositive()
        elif percentageSpeed < 0:
            self._spinNegative()
        else:
            self.turnOff()
            return
        
        #Output the PWM signal. Use the absolute value of the percentageSpeed
        self._speedControlPwmPin.duty_u16(65535 * (abs(percentageSpeed) / 100))
    
    def turnOff():
        """
        zeros everything causing the motor to halt
        """
        self._negative.value(0)
        self._positive.value(0)
        self.turnMotor(0)
