from positional_encoder import PositionalEncoder
from dc_motor import DcMotor
import time

class PidXY:
    """
    This class controls the x,y position of carriage using a PID controller.
    """
    def __init__(self, xPositionalEncoder, yPositionalEncoder, xDcMotor, yDcMotor, xMotorPidDict, yMotorPidDict, maxAllowableError):
        """
        Sets up the PidXY class. Stores two positional encoder objects as
        attributes for later use.
        
        Args:
            xPositionalEncoder: A positional encoder object that is reads the
            positional encoder on the x-axis.
            yPositionalEncoder: A positional encoder object that is reads the
            positional encoder on the y-axis
            xDcMotor: The DcMotor object that is responsible for controling the
            motor that performs x axis movement.
            yDcMotor: The DcMotor object that is responsible for controling the
            motor that performs y axis movement.
            xMotorPidDict: A dictionary containing the PID values for the x Motor
            yMotorPidDict: A dictionary containing the PID values for the y Motor
        """
        self._xPositionalEncoder = xPositionalEncoder
        self._yPositionalEncoder = yPositionalEncoder
        self._xDcMotor = xDcMotor
        self._yDcMotor = yDcMotor
        self._xMotorPidDict = xMotorPidDict
        self._yMotorPidDict = yMotorPidDict
        self._maxAllowableError = maxAllowableError
        self._controllerMax = 100
        self._controllerMin = -100
        self._atTargetCount = 0
        self._atTargetThreshold = 10
    
    def moveTo(xTarget, yTarget):
        """
        Uses a PID controler to move the carriage to the specified x and y
        position.
        
        Args:
            xTarget: The x position the cariage will attempt to move to.
            yTarget: The y position the cariage will attempt to move to.
        """
        # Init the error values to 0
        xError = 0
        yError = 0
        
        # Init the error integral values to 0
        xErrorIntegral = 0
        yErrorIntegral = 0
        
        # Used to signal the first itteration of the loop
        firstItterationFlag = True
        
        # Take the first time measurement
        currentTime = time.tick_us()
        
        # Check if the carriage is at the target
        while !self._atTarget(xError, yError):
            
            # Use the positional encoders to make a measurement
            currentX = self._xPositionalEncoder.getPosition()
            currentY = self._yPositionalEncoder.getPosition()
            
            # Record the time the the positional encoders made thier measurement
            previousTime = currentTime
            currentTime = time.tick_us()
            # Calculate the time delate and divide by 10^6 to be back to seconds
            dt = time.ticks_diff(currentTime, previousTime) / (10 ** 6)
            
            # Get the previous errors
            previousXError = xError
            previousYError = yError
            
            # Get the current errors
            xError = targetX - currentX
            yError = targetY - currentY
            
            
            if firstItterationFlag:
                # On the first itteration we cant use the integral or derivative
                # terms because there is no previous time measurement
                firstItterationFlag = False
                xControllerOutput = self._xMotorPidDict['Kp'] * xError 
                yControllerOutput = self._yMotorPidDict['Kp'] * yError
                
            else:
                # Can use the integral and derivative terms
                
                # Calculating the derivative
                xErrorDerivative = (xError - previousXError) / dt
                yErrorDerivative = (yError - previousYError) / dt
                
                # The output of the controller prior to clamping
                xIdealControllerOutput = (self._xMotorPidDict['Kp'] * xError) 
                                         + (self._xMotorPidDict['Ki'] * xErrorIntegral)
                                         + (self._xMotorPidDict['Kd'] * xErrorDerivative)
                
                yIdealControllerOutput = (self._yMotorPidDict['Kp'] * yError) 
                                         + (self._yMotorPidDict['Ki'] * yErrorIntegral)
                                         + (self._yMotorPidDict['Kd'] * yErrorDerivative)
                
                # Checking whether integral clamping is required or not
                if !self._integralClamping(xIdealControllerOutput, xError):
                    xErrorIntegral += xError * dt
                
                if !self._integralClamping(yIdealControllerOutput, yError):
                    yErrorIntegral += yError * dt
                
                # Recaculating the controller output after clamping
                xControllerOutput = (self._xMotorPidDict['Kp'] * xError) 
                                    + (self._xMotorPidDict['Ki'] * xErrorIntegral)
                                    + (self._xMotorPidDict['Kd'] * xErrorDerivative)
                
                yControllerOutput = (self._yMotorPidDict['Kp'] * yError) 
                                    + (self._yMotorPidDict['Ki'] * yErrorIntegral)
                                    + (self._yMotorPidDict['Kd'] * yErrorDerivative)
                
                # Restricting the controller within the bounds of the maximum
                # and minimum allowable values. 
                xControllerOutput = min(self._controllerMax, xControllerOutput)
                xControllerOutput = max(self._controllerMin, xControllerOutput)
                
                yControllerOutput = min(self._controllerMax, yControllerOutput)
                yControllerOutput = max(self._controllerMin, yControllerOutput)
                
                # Turn the motors
                self._xDcMotor.turnMotor(xControllerOutput)
                self._yDcMotor.turnMotor(yControllerOutput)
    
    def _integralClamping(idealControllerOutput, error):
        """

        Args:
            idealControllerOutput: The output the controller is attempting to
            drive.
            error: The error between the current and the target value.
        Returns:
            Boolean: Indicating whether integral clamping is neccessary.
        """
        # integral clamping prevents integral term from accumulating if the
        # ideal controller output is exceeding maximum or minimum of controller.
        if(idealControllerOutput >= self._controllerMax and error > 0):
            # motor going full tilt in a positive dirrection and reducing the
            # error (error is positive)
            return True
        elif(idealControllerOutput <= self._controllerMin and error < 0):
            # motor going full tilt in a negative dirrection and reducing the
            # error (error is negative)
            return True
        else
            # dont need to clamp
            return False
    
    def _atTarget(xError, yError):
        """
        Determines whether or not the carriage has arrived at the target
        position.
        
        Args:
            xError: Distance of the carriage from the target x position
            yError: Distance of the carriage from the target y position
        
        Returns:
            boolean: indicating whether or not the carriage has arrived at the
            target
        """
        
        # If the carriage is under the maximum allowable error its at the target
        # location
        if(abs(xError) <= self._maxAllowableError and abs(yError) <= self._maxAllowableError):
            self._atTargetCount += 1
            
        else:
            self._atTargetCount = 0
        
        # The target has been at the target location long enough that it has
        # been deemed to have settled there.
        if self._atTargetCount == self._atTargetThreshold:
            return True
        
        # Still not at target location
        return False
        