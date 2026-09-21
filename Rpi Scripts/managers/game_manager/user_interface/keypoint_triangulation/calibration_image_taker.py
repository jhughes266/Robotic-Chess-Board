from managers.game_manager.user_interface.keypoint_triangulation.camera import *
#from camera import *

import numpy as np
mode = 'csi'

usbCam = OpenCvDevice(captureWidth=640, captureHeight=480, deviceIndex = 0)
csiCam = PiCameraDevice(captureWidth=640, captureHeight=480, deviceIndex = 0)

usbCam.setUp()
csiCam.setUp()


numCalibrationImages = 20
for i in range(numCalibrationImages):
    input("Hit enter to take next image")
    usbImage = usbCam.captureImage()
    csiImage = csiCam.captureImage()

    combinedImage = np.hstack((csiImage, usbImage))
    cv2.imshow('capture', combinedImage)
    if mode == 'usb':
        cv2.imwrite(f"resources/calibration_images/usb_cam/cal_{i}.jpg",usbImage)
    elif mode == 'csi':
        cv2.imwrite(f"resources/calibration_images/csi_cam/cal_{i}.jpg", csiImage)

usbCam.tearDown()
csiCam.tearDown()
