import cv2
import matplotlib.pyplot as plt
import numpy as np

class KeypointTriangulator:
    def __init__(self, refCamIntrinsicDir, offsetCamIntrinsicDir):
        self.__refCameraMatrix = np.loadtxt(refCamIntrinsicDir + '/camera_matrix.txt')
        self.__offsetCameraMatrix = np.loadtxt(offsetCamIntrinsicDir + '/camera_matrix.txt')

        self.__refDistCoeffs = np.loadtxt(refCamIntrinsicDir + '/dist.txt')
        self.__offsetDistCoeffs = np.loadtxt(offsetCamIntrinsicDir + '/dist.txt')

    def run(self):
        refCameraImage, offsetCameraImage = self.__captureImages()

        refCameraImageUndistorted, newRefCameraMatrix = self.__undistortImage(refCameraImage, self.__refCameraMatrix, self.__offsetCameraMatrix)
        offsetCameraImageUndistorted, newOffsetCameraMatrix = self.__undistortImage(refCameraImage, self.__offsetCameraMatrix, self.__offsetCameraMatrix)

        self.__keypointExtraction()

        self.__triangulation()

    def __captureImages(self):
        refCamImage = None
        offsetCamImage = None
        return refCamImage, offsetCamImage

    def __undistortImage(self, image, cameraMatrix, distCoeffs):
        h, w = image.shape[:2]
        newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w, h), 1, (w, h))
        undistorted = cv2.undistort(image, cameraMatrix, distCoeffs, None, newCameraMatrix)
        x, y, w, h = roi
        croppedUndistorted = undistorted[y:y + h, x:x + w]
        return croppedUndistorted, newCameraMatrix

    def __keypointExtraction(self):
        pass

    def __triangulation(uRefCam, vRefCam, uOffsetCam, vOffsetCam, refCameraMatrix, offsetCameraMatrix, xOffset, yOffset, zOffset):

        print(offsetCameraMatrix)
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        ox = 640
        oy = 360
        fx = 3
        fy = 3

        z = np.linspace(0,10,100)
        x = (z * (uRefCam - ox)) / fx
        y = (z * (vRefCam - oy)) / fy
        ax.plot3D(x, y, z, 'red')
        plt.show()

test = KeypointTriangulator(refCamIntrinsicDir='resources/calibration_results/usb_cam', offsetCamIntrinsicDir='resources/calibration_results/csi_cam')


