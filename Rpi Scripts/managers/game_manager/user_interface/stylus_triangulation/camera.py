from config import *
from abc import ABC, abstractmethod
import time
# Conditional import. Allows running of the console based version without requiring these libraries to be installed
if USER_INTERFACE_TYPE == "stylus":
    import cv2
    from picamera2 import Picamera2


class camera(ABC):
    """
    Parent camera class. Enables different child camera classes to be created. This is needed in this project where
    I am using a USB and CSI camera.
    """
    def __init__(self, captureWidth, captureHeight, deviceIndex=0):
        """
        Initializes a camera object.
        Args:
            captureWidth: The width of the captured image in pixels.
            captureHeight: The height of the captured image in pixels.
            deviceIndex: The index of the camera device to use.
        Returns:
        """
        self._captureWidth = captureWidth
        self._captureHeight = captureHeight
        self._deviceIndex = deviceIndex

    @abstractmethod
    def setUp(self):
        """
        For acquisition and setting up of camera resources
        """
        pass

    @abstractmethod
    def tearDown(self):
        """
        For destruction and freeing of camera resources
        """
        pass

    @abstractmethod
    def captureImage(self):
        """
        For capturing an image with the camera
        """
        pass

class OpenCvDevice(camera):
    """
    A camera that uses open cv (In the case of this project that is a usb camera)
    """
    def setUp(self):
        """
        Set up the open cv camera object and get the necessary resources.
        """
        # Get the video capture device at the given index
        self.__cap = cv2.VideoCapture(self._deviceIndex)
        # This means we only get the most recent frame. We want the cameras as alligned as possible. This is particurlarly
        # the case if (like in this project) one device captures images quicker than the other.
        self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        # Set the dimensions of the capture
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._captureWidth)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._captureHeight)
        if not self.__cap.isOpened():
            print("Could not open camera")
            exit(0)

    def tearDown(self):
        """
        Free all resources used by the camera.
        """
        self.__cap.release()
        cv2.destroyAllWindows()
        del self.__cap

    def captureImage(self):
        """
        Take an image with the camera
        Returns:
            A numpy array representing the captured image.
        """
        ret, frame = self.__cap.read()
        if ret:
            return frame

        print("Could not capture image with the OPENCV device!")
        return None

class PiCameraDevice(camera):
    """
    A camera that uses open PiCamera (In the case of this project that is a csi camera)
    """
    def setUp(self):
        """
        Set up the picamera camera object and get the necessary resources.
        """
        self.__piCamera = Picamera2()
        # Format the width and height and make sure the output channels are in the right order.
        config = self.__piCamera.create_still_configuration(
            main={"size": (self._captureWidth, self._captureHeight),"format":"RGB888"},
            sensor={"output_size": (3280, 2464)})
        self.__piCamera.configure(config)
        self.__piCamera.start()

    def tearDown(self):
        """
        Free all resources used by the camera.
        """
        self.__piCamera.stop_preview()
        self.__piCamera.stop()
        self.__piCamera.close()
        del self.__piCamera

    def captureImage(self):
        """
        Take an image with the Pi camera device
        Returns:
            array = A numpy array representing the captured image.
        """
        array = None
        try:
            array = self.__piCamera.capture_array()
        except Exception as e:
            print(e)
            print("Could not capture image with the PICAMERA device!")

        return array
