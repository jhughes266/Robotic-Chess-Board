from abc import ABC, abstractmethod
#from picamera2 import Picamera2
from console_debug_info import ConsoleDebugInfo
import cv2


class camera(ABC):
    def __init__(self, deviceIndex=0):
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
        self.__piCamera = PiCamera2(camera=self._deviceIndex)
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
            ConsoleDebugInfo.printToConsole("Could not capture image with the PICAMERA device!")

        return array

class DummyPicamera2():
    def __init__(self, deviceIndex):
        ConsoleDebugInfo.printToConsole("INITIATING A DUMMY PICAMERA DEVICE PLEASE USE THE REAL PICAMERA IN THE ACTUAL SCRIPT")

    def start(self):
        ConsoleDebugInfo.printToConsole("STARTING DUMMY PICAMERA")

    def stop_preview(self):
        ConsoleDebugInfo.printToConsole("STOPPING PREVIEW FOR DUMMY PICAMERA")

    def stop(self):
        ConsoleDebugInfo.printToConsole("STOPPING DUMMY PICAMERA")

    def close(self):
        ConsoleDebugInfo.printToConsole("CLOSING DUMMY PICAMERA")

    def capture_array(self):
        #ConsoleDebugInfo.printToConsole(f"CAPTURING A DUMMY PICAMERA IMAGE")
        return None


