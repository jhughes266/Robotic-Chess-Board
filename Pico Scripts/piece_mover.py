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
            0:16, 1:24, 2:32, 3:40, 4:48, 5:56, 6:64, 7:72, 8:80, 9:88, 10:96,
            11:104
            }
        
        self.__yGridCordinateToBaseCordinates = {
            0:16, 1:24, 2:32, 3:40, 4:48, 5:56, 6:64, 7:72, 8:80, 9:88, 10:96,
            11:104
            }
        
        # There is a callibration dot on the board that should sit directly over
        # the carriage when it is moved to this location.
        calibrationX = 11
        calibrationY = 11
        
        # Disengage the gripper and move it to the callibration location ready
        # for program start
        self.moveToCalibration()
        
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
        
        def movePiece(self, startGridX, startGridY, endGridX, endGridY, engageGripper=True, disengageGripper=True):
            """
            Moves a piece from a specified starting location to a specified end
            location. You can also chose wheather the gripper gets engaged or
            disengaged at the start.
            
            Args:
                startGridX: The X pos where the piece is.
                startGridY: The Y pos where the piece is.
                endGridX: The X pos where you want the piece to end.
                endGridY: The Y pos where you want the piece to end.
                engageGripper: Enages the gripper at the start (picks the piece
                up).
                disengageGripper: Disengages the gripper at the end (drops the
                piece off).
            """
            self.moveToGridXY(startGridX, startGridY)
            
            if engageGripper:
                self.__gripper.engage()
                
            self.moveToGridXY(endGridX, endGridY)
            
            if disengageGripper:
                self.__gripper.disengage()
            
        def moveToCalibration(self):
            """
            Movea the piece the calibration location. 
            """
            self.__gripper.disengage()
            self.__pidXY.moveTo(calibrationX, calibrationY)
        
    