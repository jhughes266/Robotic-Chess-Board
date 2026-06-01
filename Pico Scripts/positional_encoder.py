from machine import Pin

class PositionalEncoder:
    """
    This class is responsible for reading the values from a positional encoder
    and changing this from a binary value into a decimal one.
    """
    def __init__(self, bitPinNumberPairList):
        """
        Inits for the PositionalEncoder class.
        
        Args:
            bitPinList: List where the key is the bit number and the value is
            the pin which corresponds to that bit.
        """
        # Save as a private attribute. They have seperate names because the init
        # method changes the data type from integers to "Pin" class objects.
        self._bitPinPairList = bitPinNumberPairList
        
        # Go through and convert all the values of the Listionary to Pin objects
        for bitNumber in range(len(self._bitPinPairList)):
            self._bitPinPairList[bitNumber] = Pin(self._bitPinPairList[bitNumber], Pin.IN)
    
    def getPosition(self)
        """
        Gets the current position of read by the positional encoder. Also converts
        it into decimal
        """
        # Stores the decimal position
        decimalPosition = 0
        
        # Loop through and read all the pins in the bitPinList accumulating the
        # value in the "decimalPosition" variable.
        for bitNumber, pin in enumerate(self._bitPinPairList):
            decimalPosition += (2 ** bitNumber) * pin.value()
        
        return decimalPosition
            
            
        
        
        

