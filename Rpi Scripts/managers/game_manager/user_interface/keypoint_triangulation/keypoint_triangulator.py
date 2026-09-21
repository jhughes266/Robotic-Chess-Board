from operator import iadd
import sympy as sp
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

        if aCamDetectionResult is None or bCamDetectionResult is None:
            return None

        self.__drawKeypoints(aCamDetectionResult, aCamImage)
        self.__drawKeypoints(bCamDetectionResult, bCamImage)

        combinedImage = np.hstack((aCamImage, bCamImage))

        cv2.imshow('capture', combinedImage)

        landMarkRealWorldLocation = self.__triangulePoints(aCamDetectionResult=aCamDetectionResult, bCamDetectionResult=bCamDetectionResult,
                               aNewCamMatrix=aNewCamMatrix , bNewCamMatrix=bNewCamMatrix, offset=(1,2,3))
        return landMarkRealWorldLocation

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
        oya = aNewCamMatrix[1][2]

        fxb = bNewCamMatrix[0][0]
        fyb = bNewCamMatrix[1][1]
        oxb = bNewCamMatrix[0][2]
        oyb = bNewCamMatrix[1][2]

        landMarkRealWorldLocation = []

        for i, (aCamLandmark, bCamLandmark) in enumerate(zip(aCamDetectionResult.hand_landmarks[0], bCamDetectionResult.hand_landmarks[0])):

            # Get the location of the landmark for camera a
            ua = aCamLandmark.x
            va = aCamLandmark.y
            # Get the location of the landmark for camera b
            ub = bCamLandmark.x
            vb = bCamLandmark.y
            # calculate the components of the a direction vector
            ia = (ua - oxa) / fxa
            ja = (va - oya) / fya
            ka = 1
            # calculate the components of the b direction vector
            ib = (ub - oxb) / fxb
            jb = (vb - oyb) / fyb
            kb = 1
            # Constructing the direction vectors
            aDir = np.array([ia, ja, ka])
            bDir = np.array([ib, jb, kb])
            # Construct the position vector for b (this is the offset) we assume that a starts at (0,0,0)
            bPos = np.array([xOffset, yOffset, zOffset])
            # Calculating the different quantities for the triangulation equations
            P = np.sum(aDir * aDir)
            S = np.sum(aDir * bDir)
            R = np.sum(aDir * bPos)
            T = np.sum(bDir * bDir)
            U = np.sum(bDir * bPos)
            # Using the calculated simultaneous equations to get the parameters
            denominator = P*T - S**2
            ta = (R*T - S*U)/denominator
            tb = (S*R - P*U)/denominator
            # Using the parameters to construct the line equations and get the locations of the minimum distance between lines
            aLocMin = ta * aDir
            bLocMin = tb * bDir + bPos
            # Getting the average of the two to get the best estimate of the location of the minimum distance
            estimatedMinimumDistancePoint = (aLocMin + bLocMin) / 2
            # Storing the result in created list
            landMarkRealWorldLocation.append(estimatedMinimumDistancePoint)
        # Returning the real world location of the landmarks
        return landMarkRealWorldLocation




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


ta, tb, P, Q, R, S, T, U = sp.symbols("ta tb P Q R S T U")

eq1 = sp.Eq(ta*P - tb*Q - R,0)
eq2 = sp.Eq(-ta*S + tb*T + U,0)

solution = sp.solve((eq1, eq2), (ta, tb))
print(solution)

testCam1 = OpenCvDevice(captureWidth=640, captureHeight=480, deviceIndex=0)
#testCam2 = OpenCvDevice(captureWidth=640, captureHeight=480, deviceIndex=0)
testTri = KeypointTriangulator(aCamObj=testCam1, bCamObj=testCam1,aCamIntrinsicDir='resources/calibration_results/usb_cam', bCamIntrinsicDir='resources/calibration_results/csi_cam')
testTri.setUp()

while True:
    ### For debugging ####
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    landmarkLocations = testTri.run()
    print(landmarkLocations)


testTri.tearDown()


