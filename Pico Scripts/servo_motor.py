from machine import Pin
from machine import PWM

class ServoMotor:
    """
    This class controls the angle of a servo motor
    """
    def __init__(self, angleControlPinNumber):
        """
        This class enables control of the servo on the pico.
        
        Args:
            angleControlPinNumber: The pin that is used to output the PWM signal
            that will control the servo.
        """
        # Init the PWM pin
        self.__servoPwmPin = PWM(Pin(angleControlPinNumber))
        # Set the PWM frequency to the frequency required by the servo
        pwmFrequency = 50
        self.__servoPwmPin.freq(pwmFrequency)
        # All values are in ms
        self.__pwmPeriod = 20.000
        self.__min_pulse_width = 1.000
        self.__max_pulse_width = 2.000
        
        
    def angle(self, angle):
        """
        Puts the servo to the specified angle.
        
        Args:
            angle: The angle that you want the servo to go to.
        """
        # Proportion of the 180 deg that you want the servo to go to.
        proportionOfFullRange = angle / 180
        # The pulse width required to get the desired angle
        pulseWidth = self.__min_pulse_width + ((proportionOfFullRange) * (self.__max_pulse_width - self.__min_pulse_width))
        # Get the PWM value required by the pico
        picoPwmValue = int((pulseWidth / self.__pwmPeriod) * 65535)
        # Send the PWM to the pin
        self.__servoPwmPin.duty_u16(picoPwmValue)
    
    def turnOff(self):
        """
        Turn the servo off. This may cause the servo to go limp.
        """
        self.__servoPwmPin.duty_u16(0)
        
        