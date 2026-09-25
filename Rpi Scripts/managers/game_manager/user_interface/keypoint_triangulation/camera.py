from abc import ABC, abstractmethod
from picamera2 import Picamera2
from console_debug_info import ConsoleDebugInfo
import cv2


class camera(ABC):
    def __init__(self, captureWidth, captureHeight, deviceIndex=0):
        self._captureWidth = captureWidth
        self._captureHeight = captureHeight
        self._deviceIndex = deviceIndex

    @abstractmethod
    def setUp(self):
        pass

    @abstractmethod
    def tearDown(self):
        pass

    @abstractmethod
    def captureImage(self):
        pass

class OpenCvDevice(camera):
    def setUp(self):
        self.__cap = cv2.VideoCapture(self._deviceIndex)
        self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._captureWidth)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._captureHeight)
        if not self.__cap.isOpened():
            ConsoleDebugInfo.printToConsole("Could not open camera")
            exit(0)

    def tearDown(self):
        self.__cap.release()
        cv2.destroyAllWindows()
        del self.__cap

    def captureImage(self):
        ret, frame = self.__cap.read()
        if ret:
            return frame

        ConsoleDebugInfo.printToConsole("Could not capture image with the OPENCV device!")
        return None

class PiCameraDevice(camera):
    def setUp(self):
        self.__piCamera = Picamera2()
        config = self.__piCamera.create_still_configuration(
            main={"size": (self._captureWidth, self._captureHeight),"format":"RGB888"},
            sensor={"output_size": (3280, 2464)})
        self.__piCamera.configure(config)
        self.__piCamera.start()

    def tearDown(self):
        self.__piCamera.stop_preview()
        self.__piCamera.stop()
        self.__piCamera.close()
        del self.__piCamera

    def captureImage(self):
        array = None
        try:
            array = self.__piCamera.capture_array()
        except Exception as e:
            ConsoleDebugInfo.printToConsole(e)
            ConsoleDebugInfo.printToConsole("Could not capture image with the PICAMERA device!")

        return array
