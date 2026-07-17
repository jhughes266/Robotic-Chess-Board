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
            minControllerOutput: The minimum the controller can output. The
            original output of the controller will be scalled between this value
            and 100%
        """
        self.__xPositionalEncoder = xPositionalEncoder
        self.__yPositionalEncoder = yPositionalEncoder
        self.__xDcMotor = xDcMotor
        self.__yDcMotor = yDcMotor
        self.__xMotorPidDict = xMotorPidDict
        self.__yMotorPidDict = yMotorPidDict
        self.__maxAllowableError = maxAllowableError
        self.__controllerMax = 100
        self.__controllerMin = -100
        self.__atTargetCount = 0
        self.__atTargetThreshold = 500
    
    def moveTo(self, targetX, targetY):
        """
        Uses a PID controler to move the carriage to the specified x and y
        position.
        
        Args:
            targetX: The x position the cariage will attempt to move to.
            targetY: The y position the cariage will attempt to move to.
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
        currentTime = time.ticks_us()
        
        # Check if the carriage is at the target
        iter_count = 0
        while not self.__atTarget(xError, yError):
            iter_count += 1
            # Use the positional encoders to make a measurement
            currentX = self.__xPositionalEncoder.getPosition()
            currentY = self.__yPositionalEncoder.getPosition()  
            
            # Record the time the the positional encoders made thier measurement
            previousTime = currentTime
            currentTime = time.ticks_us()
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
                xControllerOutput = self.__xMotorPidDict['Kp'] * xError 
                yControllerOutput = self.__yMotorPidDict['Kp'] * yError
                
            else:
                # Can use the integral and derivative terms
                
                # Calculating the derivative
                xErrorDerivative = (xError - previousXError) / dt
                yErrorDerivative = (yError - previousYError) / dt
                
                # The output of the controller prior to clamping
                xIdealControllerOutput = ((self.__xMotorPidDict['Kp'] * xError) 
                                         + (self.__xMotorPidDict['Ki'] * xErrorIntegral)
                                         + (self.__xMotorPidDict['Kd'] * xErrorDerivative))
                
                yIdealControllerOutput = ((self.__yMotorPidDict['Kp'] * yError) 
                                         + (self.__yMotorPidDict['Ki'] * yErrorIntegral)
                                         + (self.__yMotorPidDict['Kd'] * yErrorDerivative))
                
                # Checking whether integral clamping is required or not
                if not self.__integralClamping(xIdealControllerOutput, xError):
                    xErrorIntegral += xError * dt
                
                if not self.__integralClamping(yIdealControllerOutput, yError):
                    yErrorIntegral += yError * dt
                
                # Recaculating the controller output after clamping
                xControllerOutput = ((self.__xMotorPidDict['Kp'] * xError) 
                                    + (self.__xMotorPidDict['Ki'] * xErrorIntegral)
                                    + (self.__xMotorPidDict['Kd'] * xErrorDerivative))
                
                yControllerOutput = ((self.__yMotorPidDict['Kp'] * yError) 
                                    + (self.__yMotorPidDict['Ki'] * yErrorIntegral)
                                    + (self.__yMotorPidDict['Kd'] * yErrorDerivative))
                                    
                
                
                
                # Restricting the controller within the bounds of the maximum
                # and minimum allowable values. 
                xControllerOutput = min(self.__controllerMax, xControllerOutput)
                xControllerOutput = max(self.__controllerMin, xControllerOutput)
                
                yControllerOutput = min(self.__controllerMax, yControllerOutput)
                yControllerOutput = max(self.__controllerMin, yControllerOutput)
                
                # For testing
                if iter_count % 100 == 0:
                    print("X |Pos: " + str(currentX) +  " Error: " + str(xError) + " Controller Out: " + str(xControllerOutput))
                    print("Y |Pos: " + str(currentY) +  " Error: " + str(yError) + " Controller Out: " + str(yControllerOutput))

                
                # Turn the motors
                self.__xDcMotor.turnMotor(xControllerOutput)
                self.__yDcMotor.turnMotor(yControllerOutput)
                
                
    
    def __integralClamping(self, idealControllerOutput, error):
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
        if(idealControllerOutput >= self.__controllerMax and error > 0):
            # motor going full tilt in a positive dirrection and reducing the
            # error (error is positive)
            return True
        elif(idealControllerOutput <= self.__controllerMin and error < 0):
            # motor going full tilt in a negative dirrection and reducing the
            # error (error is negative)
            return True
        else:
            # dont need to clamp
            return False
    
    def __atTarget(self, xError, yError):
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
        if(abs(xError) <= self.__maxAllowableError and abs(yError) <= self.__maxAllowableError):
            self.__atTargetCount += 1            
        else:
            self.__atTargetCount = 0
        
        # The target has been at the target location long enough that it has
        # been deemed to have settled there.
        if self.__atTargetCount == self.__atTargetThreshold:
            # Reset the target count
            self.__atTargetCount = 0
            # Turn the motors off
            self.__xDcMotor.turnOff()
            self.__yDcMotor.turnOff()
            return True
        
        # Still not at target location
        return False
        