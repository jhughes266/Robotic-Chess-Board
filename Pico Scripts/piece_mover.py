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
            0:13, 1:21, 2:31, 3:39, 4:47, 5:55, 6:63, 7:71, 8:79, 9:87, 10:98,
            11:106
            }
        
        self.__yGridCordinateToBaseCordinates = {
            0:12, 1:20, 2:31, 3:39, 4:48, 5:55, 6:63, 7:72, 8:79, 9:87, 10:99,
            11:107
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

