from operator import iadd

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import Image, ImageFormat
import matplotlib.pyplot as plt
import numpy as np
from mediapipe.tasks.python.vision.drawing_utils import draw_landmarks

from managers.game_manager.user_interface.keypoint_triangulation.camera import *

class KeypointTriangulator:
    def __init__(self, aCamObj, bCamObj, aCamIntrinsicDir, bCamIntrinsicDir):
        self.__aCamObj = aCamObj
        self.__bCamObj = bCamObj

        self.__aCamMatrix = np.loadtxt(aCamIntrinsicDir + '/camera_matrix.txt')
        self.__bCamMatrix = np.loadtxt(bCamIntrinsicDir + '/camera_matrix.txt')

        self.__aDistCoeffs = np.loadtxt(aCamIntrinsicDir + '/dist.txt')
        self.__bDistCoeffs = np.loadtxt(bCamIntrinsicDir + '/dist.txt')

    def setUp(self):
        self.__aCamObj.setUp()
        self.__bCamObj.setUp()
        base_options = python.BaseOptions(model_asset_path='resources/hands_model/hand_landmarker.task')
        options = vision.HandLandmarkerOptions(base_options=base_options,
                                               min_hand_detection_confidence=0.8,
                                               min_hand_presence_confidence=0.8,
                                               min_tracking_confidence=0.8,
                                               num_hands=1)
        self.__detector = vision.HandLandmarker.create_from_options(options=options)

    def tearDown(self):
        self.__aCamObj.tearDown()
        self.__bCamObj.tearDown()

    def run(self):
        aCamImage, bCamImage = self.__captureImages()

        aCamImageUndistorted, aNewCamMatrix = self.__undistortImage(aCamImage, self.__aCamMatrix, self.__aDistCoeffs)
        bCamImageUndistorted, bNewCamMatrix = self.__undistortImage(bCamImage, self.__bCamMatrix, self.__bDistCoeffs)

        aCamDetectionResult, bCamDetectionResult = self.__keypointExtraction(aCamImageUndistorted, bCamImageUndistorted)

        ### For debugging ####
        if aCamDetectionResult != None or bCamDetectionResult != None:
            self.__drawKeypoints(aCamDetectionResult, aCamImage)
            self.__drawKeypoints(bCamDetectionResult, bCamImage)

        combinedImage = np.hstack((aCamImage, bCamImage))

        cv2.imshow('capture', combinedImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        ######################

        self.__triangulePoints(aCamDetectionResult=aCamDetectionResult, bCamDetectionResult=bCamDetectionResult,
                               aNewCamMatrix=aNewCamMatrix , bNewCamMatrix=bNewCamMatrix, offset=(0,0,0))
        return True

    def __captureImages(self):
        aCamImage = self.__aCamObj.captureImage()
        bCamImage = self.__bCamObj.captureImage()

        return aCamImage, bCamImage

    def __undistortImage(self, image, camMatrix, distCoeffs):
        h, w = image.shape[:2]
        newCamMatrix, roi = cv2.getOptimalNewCameraMatrix(camMatrix, distCoeffs, (w, h), 1, (w, h))
        undistorted = cv2.undistort(image, camMatrix, distCoeffs, None, newCamMatrix)
        x, y, w, h = roi
        croppedUndistorted = undistorted[y:y + h, x:x + w]
        return croppedUndistorted, newCamMatrix

    def __keypointExtraction(self, aCamImage, bCamImage):
        aCamImageRgb = cv2.cvtColor(aCamImage, cv2.COLOR_BGR2RGB)
        bCamImageRgb = cv2.cvtColor(bCamImage, cv2.COLOR_BGR2RGB)

        aCamMpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=aCamImageRgb)
        bCamMpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=bCamImageRgb)

        aCamDetectionResult = self.__detector.detect(aCamMpImage)
        bCamDetectionResult = self.__detector.detect(bCamMpImage)

        if len(aCamDetectionResult.hand_landmarks) == 0 or len(bCamDetectionResult.hand_landmarks) == 0:
            return None, None

        # Put the x and y coordinates in pixels
        aCamDetectionResult = self.__normalizedCordinatesToPixel(results=aCamDetectionResult,
                                                                 xDim=aCamImage.shape[1],
                                                                 yDim=bCamImage.shape[0])

        bCamDetectionResult = self.__normalizedCordinatesToPixel(results=bCamDetectionResult,
                                                                   xDim=aCamImage.shape[1],
                                                                   yDim=bCamImage.shape[0])



        return aCamDetectionResult, bCamDetectionResult

    def __triangulePoints(self, aCamDetectionResult, bCamDetectionResult , aNewCamMatrix, bNewCamMatrix, offset):
        xOffset = offset[0]
        yOffset = offset[1]
        zOffset = offset[2]

        fxa = aNewCamMatrix[0][0]
        fya = aNewCamMatrix[1][1]
        oxa = aNewCamMatrix[0][2]
        oxb = aNewCamMatrix[1][2]

        fxb = bNewCamMatrix[0][0]
        fyb = bNewCamMatrix[1][1]
        oxb = bNewCamMatrix[0][2]
        oxb = bNewCamMatrix[1][2]

        for aCamLandmark, bCamLandmark in zip(aCamDetectionResult.hand_landmarks[0], bCamDetectionResult.hand_landmarks[0]):


        """
        ia = 
        ja =
        ka =

        ib =
        jb =
        kb =
        
        
        
        print(bCamMatrix)
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
        """

    def __normalizedCordinatesToPixel(self, results, xDim, yDim):
        landmarkList = results.hand_landmarks[0]
        for landmark in landmarkList:
            landmark.x = landmark.x * xDim
            landmark.y = landmark.y * yDim
        return results

    def __drawKeypoints(self, results, image):
        hand_landmarks_list = results.hand_landmarks
        #print(results.handedness)
        if len(hand_landmarks_list) > 0:
            for hand in hand_landmarks_list:
                for landmark in hand:
                    cv2.circle(image, (int(landmark.x), int(landmark.y)), 5, (0, 0, 255), -1)

testCam1 = OpenCvDevice(0)
#testCam2 = OpenCvDevice(0)
testTri = KeypointTriangulator(aCamObj=testCam1, bCamObj=testCam1,aCamIntrinsicDir='resources/calibration_results/usb_cam', bCamIntrinsicDir='resources/calibration_results/csi_cam')
testTri.setUp()

while testTri.run():
    pass

testTri.tearDown()


