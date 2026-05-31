from positional_encoder import PositionalEncoder
import time

class PidXY:
    """
    This class controls the x,y position of carriage using a PID controller.
    """
    def __init__(self, xPositionalEncoder, yPositionalEncoder):
        """
        Sets up the PidXY class. Stores two positional encoder objects as
        attributes for later use.
        
        Args:
        xPositionalEncoder: A positional encoder object that is reads the
        positional encoder on the x-axis.
        yPositionalEncoder: A positional encoder object that is reads the
        positional encoder on the y-axis
        """
        self._xPositionalEncoder = xPositionalEncoder
        self._yPositionalEncoder = yPositionalEncoder