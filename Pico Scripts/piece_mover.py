from pid_xy import PidXY

class PieceMover:
    """
    This class is responsible for moving pieces from one grid location to
    another.
    """
    def __init__(self, pidXY, gripper):
        """
        Inits for the PieceMover class.
        
        Args:
            pidXY: The pid controller class that can controll the x,y location
            of the carriage
            gripper: The object that controls the gripper.
        """
        self.__pidXY = pidXY
        self.__gripper = gripper
        # Dictionaries that convert the grid cordinates to the underlying
        # cordinates that the PID controller can use. This could be done with a
        # simple mathmatical calculation but the dictionary enable us to account
        # for offsets that may need to be put in. Can potentially just change
        # this to a math equation later if that is approriate.
        self.__xGridCordinateToBaseCordinates = {
            0:17, 1:25, 2:34, 3:42, 4:50, 5:58, 6:66, 7:74, 8:82, 9:90, 10:98,
            11:106
            }
        
        self.__yGridCordinateToBaseCordinates = {
            0:16, 1:24, 2:33, 3:41, 4:49, 5:58, 6:66, 7:74, 8:82, 9:91, 10:99,
            11:106
            }
        
        # There is a callibration dot on the board that should sit directly over
        # the carriage when it is moved to this location.
        self.__calibrationX = 11
        self.__calibrationY = 11
    
    def moveToGridXY(self, gridX, gridY):
        """
        Moves the carriage to a specified X,Y location within the grid.
        
        Args:
            gridX: The x location in the grid where the carriage is to be
            moved
            gridY:The y location in the grid where the carriage is to be
            moved
        """
        self.__pidXY.moveTo(
            self.__xGridCordinateToBaseCordinates[gridX],
            self.__yGridCordinateToBaseCordinates[gridY]
            )
    
    def engageGripper(self):
        """
        Engages the gripper.
        """
        self.__gripper.engage()
    
    def disengageGripper(self):
        """
        Diengages the gripper.
        """
        self.__gripper.disengage()
        
    def moveToCalibration(self):
        """
        Movea the piece the calibration location. 
        """
        self.__gripper.disengage()
        self.__pidXY.moveTo(self.__calibrationX, self.__calibrationY)

