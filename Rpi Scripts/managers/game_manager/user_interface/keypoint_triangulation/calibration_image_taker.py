from managers.game_manager.user_interface.keypoint_triangulation.camera import *

import numpy as np

usbCam = OpenCvDevice(0)
csiCam = PiCameraDevice(0)

usbCam.setUp()
csiCam.setUp()

usbImage = usbCam.captureImage()
csiImage = usbCam.captureImage()

combinedImage = np.hstack((csiImage, csiImage))
cv2.imshow('capture', combinedImage)
if cv2.waitKey(0) & 0xFF == ord('q'):
    pass

usbCam.tearDown()
csiCam.tearDown()
